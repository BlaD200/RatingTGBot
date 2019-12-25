import platform

import requests
import os
import datetime

from schedule import schedules_dir
from schedule.scheduler_link_parser import parse_links
from sql import initialize_connection


def download(url: str, filename: str) -> bool:
    """
    Download the file from giving url and place into /schedules/[filename]
    :param url: the url from which file will be loaded
    :param filename: name of the fle that will be placed on dick
    :return: true if if downloaded and saved file successfully else false
    """
    r = requests.get(url)
    if r.status_code != 200:
        return False

    with open(r'%s/%s' % (schedules_dir, filename), 'wb') as f:
        f.write(r.content)
    return True


def update_schedules():
    urls = parse_links()

    db = initialize_connection()
    cursor = db.cursor()
    cursor.execute("SELECT schedule_name FROM update_info")
    result = cursor.fetchall()
    files = list()
    for x in result:
        files.append(x[0])

    for schedule in urls:
        filename = r'%s/%s' % (schedules_dir, schedule)
        cursor.execute("SELECT last_update FROM update_info WHERE schedule_name = %s;", ("first",))
        last_update = cursor.fetchall()
        if last_update:
            last_update = last_update[0][0]
        if schedule not in files or (last_update and last_update < urls[schedule][1]):
            download(urls[schedule][0], filename)
            cursor.execute("INSERT INTO update_info(schedule_name, url_to_schedule, last_update) VALUES (%s, %s, %s)",
                           (schedule, urls[schedule][0], str(datetime.datetime.now()).split(".")[0]))
            db.commit()


def creation_date(path_to_file: str) -> datetime.datetime:
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        str_date = datetime.datetime.fromtimestamp(os.path.getctime(path_to_file)).strftime('%Y-%m-%d %H:%M:%S')
        return datetime.datetime.fromisoformat(str_date)
    else:
        stat = os.stat(path_to_file)
        try:
            str_date = datetime.datetime.fromtimestamp(stat.st_birthtime).strftime('%Y-%m-%d %H:%M:%S')
            return datetime.datetime.fromisoformat(str_date)
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            str_date = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            return datetime.datetime.fromisoformat(str_date)


if __name__ == '__main__':
    update_schedules()
    pass

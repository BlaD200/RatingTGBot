import platform

import requests
import os
import datetime

from web_processing import timetables_dir
from web_processing.timetables_link_parser import parse_links
from sql import initialize_connection, update_last_index


def download(url: str, filename: str) -> bool:
    """
    Download the file from giving url and place into /timetables/[filename]
    :param url: the url from which file will be loaded
    :param filename: name of the fle that will be placed on dick
    :return: true if if downloaded and saved file successfully else false
    """
    r = requests.get(url)
    if r.status_code != 200:
        return False

    with open(r'%s/%s' % (timetables_dir, filename), 'wb') as f:
        f.write(r.content)
    return True


def update_timetables():
    """
    Downloads timetables from urls are given by the function :ref:`timetable_link_parser`
    if they updated on site after last local update and yields downloaded filename

    :return: generator through each downloaded file
    """
    urls = parse_links()

    db = initialize_connection()
    cursor = db.cursor()

    update_last_index(db, "update_info", "timetable_id")

    cursor.execute("SELECT timetable_name FROM update_info")
    result = cursor.fetchall()
    files = list()
    for x in result:
        files.append(x[0])

    for timetable in urls:
        filename = r'%s/%s' % (timetables_dir, timetable)
        cursor.execute("SELECT last_update FROM update_info WHERE timetable_name = %s;", ("first",))
        last_update = cursor.fetchall()
        if last_update:
            last_update = last_update[0][0]
        if timetable not in files or (last_update and last_update < urls[timetable][1]):
            if download(urls[timetable][0], filename):
                cursor.execute("INSERT INTO update_info(timetable_name, url_to_timetable, last_update, faculty_name, isMP)"
                               " VALUES (%s, %s, %s, %s, %s)",
                               (timetable, urls[timetable][0], str(datetime.datetime.now()).split(".")[0],
                                urls[timetable][2], urls[timetable][3]))
                db.commit()
                print("Downloaded... ||{:<100s}||".format(timetable))
                yield timetable

    db.close()


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
    list(update_timetables())
    pass

from bs4 import BeautifulSoup
import requests
import datetime


def parse_links() -> dict:
    """
    Used to get links to all available timetables
    :return: dictionary formed ad {"<timetabler name>" : ["<url to download>", "update date"]}, where "update date" is
    last update on site
    """
    r = requests.get("https://my.ukma.edu.ua/timetable")
    if r.status_code == 200:
        urls = dict()
        soup = BeautifulSoup(r.text, "html.parser")
        faculty_list = soup.find(id="timetable-accordion")
        for faculty in faculty_list.find_all('div', {"class": "panel panel-info"}):
            faculty_name = faculty.div.h4.a.text.strip()
            for year in faculty.div.next_sibling.next_sibling.div.div('div', {'class': 'panel panel-default'}):
                mp = year.div.h4.a.text.strip()
                mp = True if "МП" in mp else False
                for speciality in year('li'):
                    speciality_name = speciality('a')[-1].text.strip()
                    date = speciality.div.span.text.strip()
                    date = datetime.datetime(*list(reversed([int(x) for x in date.split(' ')[1].split('.')])) +
                                              [int(x.replace(')', '')) for x in date.split(' ')[-1].split(':')])
                    url = speciality('a')[-1]['href'].strip()
                    urls[speciality_name] = [url, date, faculty_name, mp]
        return urls
    else:
        return None


if __name__ == '__main__':
    urls = parse_links()
    for key in urls:
        print(key, ':', urls[key])

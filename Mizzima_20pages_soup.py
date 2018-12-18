import bs4
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from fake_useragent import UserAgent
import csv
import sys

ua = UserAgent()
headers = {'User-Agent': str(ua.random)}
print(headers)

urls = [
    "http://www.mizzimaburmese.com/article/53173",
    "http://www.mizzimaburmese.com/article/53172",
    "http://www.mizzimaburmese.com/article/53171",
    "http://www.mizzimaburmese.com/article/53167",
    "http://www.mizzimaburmese.com/article/53165",
    "http://www.mizzimaburmese.com/article/53164",
    "http://www.mizzimaburmese.com/article/53160",
    "http://www.mizzimaburmese.com/article/53174",
    "http://www.mizzimaburmese.com/article/53169",
    "http://www.mizzimaburmese.com/article/52168",
    "http://www.mizzimaburmese.com/article/24235",
    "http://www.mizzimaburmese.com/article/24252",
    "http://www.mizzimaburmese.com/article/24331",
    "http://www.mizzimaburmese.com/article/24369",
    "http://www.mizzimaburmese.com/article/24419",
    "http://www.mizzimaburmese.com/article/24421",
    "http://www.mizzimaburmese.com/article/24424",
    "http://www.mizzimaburmese.com/article/24432",
    "http://www.mizzimaburmese.com/article/24441",
    "http://www.mizzimaburmese.com/article/24448",
    "http://www.mizzimaburmese.com/article/24452",
]

for url in urls:
    
    print("Processing {}".format(url))
    extracted_content = []

    req = Request(url, headers)
    page_html = urlopen(req).read()
    page_soup = soup(page_html, "html.parser")
    date_container = page_soup.findAll(
        "span", {"class": "date-display-single"})

    if date_container == []:
        break

    date = date_container[0].text

    headtext_container = page_soup.findAll(
        "div", {"class": "news-details-title"})

    if headtext_container == []:
        break

    headtext = headtext_container[0].text
    extracted_content.append(str(headtext))

    bodytext_container = page_soup.find(
        "div", {"class": "field-item even"}, {"property": "content:encoded"})

    if bodytext_container == []:
        break

    [s.extract() for s in bodytext_container('script')]
    [s.extract() for s in bodytext_container('div')]

    bodytext_container = bodytext_container.find_all("p", {"class": None})

    for body in bodytext_container:
        extracted_content.append(str(body.text))

    #extracted_content.append(str(date)) # Don't want to add date: Eng language
    with open("C:\myanmar-website-crawlers\Mizzima_20pages_data.csv", "a", encoding='utf-8') as WR:
        writer = csv.writer(WR)
        for item in extracted_content:
            writer.writerow([item])

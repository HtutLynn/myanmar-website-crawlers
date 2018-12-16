from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import csv

presidentOffice = "ggwp"
ua = UserAgent()
headers = {'User-Agent': str(ua.random)}
print(headers)

urls = [presidentOffice]
contents = []
titles = []
count = 0
for url in urls:
    if(count != 31):

        print("Processing {}".format(url))
        page = urlopen(url).read()
        soup = BeautifulSoup(page, "lxml")

        h4s = soup.find_all("span", attrs={'id': 'story_date'})

        if h4s == []:
            break

        for h4 in h4s:
            for text in h4.find_next_siblings(text=True):
                if text != ' ':
                    contents.append(text.strip())

        for span in soup.findAll('span', attrs={'class': 'no_media'}):
            titles.append(span.contents[0])
    count += 1
#rows = zip(titles, contents)
rows = zip(titles)

with open("2010.csv", "w", newline='', encoding='utf-8-sig') as csvfile:
    print("Writing to csv...")
    writer = csv.writer(csvfile)
    for row in rows:
        writer.writerow(row)
    # for row in rows:
    #     writer.writerow(row)

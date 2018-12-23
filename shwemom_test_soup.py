import bs4
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from fake_useragent import UserAgent
import csv
import sys

ua = UserAgent()
headers = {'User-Agent': str(ua.random)}

# Put the desired url or website into the variable
my_url = "http://www.shwemom.com/celebrities-and-their-phobias-v2/"
# pre-build a free list for final extracted content
extracted_content = []

# This requires a free list since mmtimes website is inconsistent
final_content = []

# because of mod_security or some similar server security feature
# which blocks known spider/bot user agents (urllib uses something like python urllib/3.3.0,
# it's easily detected)
# So, We are gonna try it by sending a formal request
# with known browser agent in this case Mozilla
# If you send numerous request to server using just crawler and this ip-address
# It can get you banned so take care!
req = Request(my_url, headers=headers)

# save the html file into a container : page_html
page_html = urlopen(req).read()

# Then parse html using soup function of the bautifulSoup library
# we can parse in many different ways : XML for example
# The data structure type of resulted output is beautifulSoup
# beautifulSoup data structure can let us access the html file effortlessly
page_soup = soup(page_html, "html.parser")

print()

# In order to work this type of script
# This website must use standardized HTML format
# From now, we will extract four things
# Date of the article, Type of news, Head text of the article and the content

# First, we must find all the div function that contain the info that we need
# For that, we need to use findAll function fory all desired html tag : <div> for example
# using just page_soup.div will only give the first one div tag

# The headtext of the article in shwemom website is in <div> so extract that
headtext_container = page_soup.findAll("h1", {"class": "entry-title"})

# In case there's no matched item, then exit!
if headtext_container == []:
    print("There's no item in headtext_container")
    sys.exit()
else:
    # add the scraped text into final extracted content
    for headtext in headtext_container:
        extracted_content.append(str(headtext.text))

content_container = page_soup.find("div", {"class": "td-post-content"})

[s.extract() for s in content_container('div')]
[s.extract() for s in content_container('blockquote')]
[s.extract() for s in content_container('script')]
[s.extract() for s in content_container('img')]

if content_container == []:
    print("There's no item in the content_container")
    sys.exit()  # Alternative : if not date_container: works too
else:
    # print(content_container)

    #[s.extract() for s in content_container('br')]

    content_container = content_container.find_all("p", {"class": None})

    for content in content_container:
        test = []

        # print(content_container)
        for temp in content.childGenerator():
            test.append(temp)

        for entry in test:
            if isinstance(entry, bs4.NavigableString):
                extracted_content.append(str(entry).strip())
            elif isinstance(entry, bs4.Tag):
                pass

    for text in extracted_content:
        if not text:
            pass
        else:
            final_content.append(text)

    # Delete last entry beacuse it's in english and about source news
    del final_content[-1]

    # deleting the None type empty content in finalized list which is about to write
    final_content = list(filter(None,final_content))

    with open("C:\myanmar-website-crawlers\shwemom_data.csv", "w", encoding='utf-8') as WR:
        writer = csv.writer(WR)
        for item in final_content:
            writer.writerow([item])  # Need to add [] for item because without it,
            # the writer function will store each charaters and syllables as a column

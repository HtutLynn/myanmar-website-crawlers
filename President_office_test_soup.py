import bs4
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from fake_useragent import UserAgent
import csv
import sys


ua = UserAgent()
headers = {'User-Agent': str(ua.random)}

# Put the desired url or website into the variable
#my_url = "http://www.president-office.gov.mm/?q=briefing-room/news/2018/12/15/id-14831"
my_url = "http://www.president-office.gov.mm/?q=briefing-room/news/2018/12/15/id-14831"

# pre-build a free list for extracted content
extracted_content = []

# pre-build a free list for final content
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

# In order to work this type of script
# This website must use standardized HTML format
# From now, we will extract four things
# Date of the article, Type of news, Head text of the article and the content

# First, we must find all the div function that contain the info that we need
# For that, we need to use findAll function fory all desired html tag : <div> for example
# using just page_soup.div will only give the first one div tag

# The headtext of the article in president website is in <h1> so extract that
headtext_container = page_soup.findAll("h1", {"class": "page-title"})

# In case there's no matched item, then exit!
if headtext_container == []:
    print("There's no item in headtext_container")
    sys.exit()
else:
    # add the scraped text into final extracted content
    for headtext in headtext_container:
        extracted_content.append(str(headtext.text))

# President office website has all main contents including date under a div
# Extract the all contents from the tag
# And dump the information into content_container
# There are many tag with "class" : "field-item even" so just use preoperty tag to filter
content_container = page_soup.find("div", {"property": "content:encoded"})

# In case there's no matched item, then exit!
if content_container == []:
    print("There's no item in the content_container")
    sys.exit()  # Alternative : if not date_container: works too
else:
    # all tag within the filtered tags are all <p> so select them all to scrape
    # all <p> don't have class so assign it None
    content_container = content_container.find_all("p", {"class": None})

    # And save the information into extracted_content by loop
    for content in content_container:
        extracted_content.append(str(content.text))

    # The first <p> in body content is always empty so delete it
    for entry in extracted_content:
        if not entry:
            pass
        else:
            final_content.append(entry)

    # deleting the None type empty content in finalized list which is about to write
    final_content = list(filter(None,final_content))

    # Write the extracted content into csv file
    with open("C:\myanmar-website-crawlers\President_office_data.csv", "w", encoding='utf-8') as WR:
        writer = csv.writer(WR)
        for item in final_content:
            writer.writerow([item])  # Need to add [] for item because without it,
            # the writer function will store each charaters and syllables as a column
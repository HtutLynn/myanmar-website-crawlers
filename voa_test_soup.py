import bs4
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from fake_useragent import UserAgent
import csv
import sys

ua = UserAgent()
headers = {'User-Agent': str(ua.random)}

NoneType = type(None) # for 'NoneTpye' specific error avoidance

# Put the desired url or website into the variable
my_url = "https://burmese.voanews.com/a/american-burmese-christmas-in-unitedstates-/4714508.html"

# pre-build a free list for final extracted content
extracted_content = []

# pre-build a container for dates
dates = []

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

# In order to work this type of script
# This website must use standardized HTML format
# From now, we will extract four things
# Date of the article, Type of news, Head text of the article and the content

# First, we must find all the div function that contain the info that we need
# For that, we need to use findAll function fory all desired html tag : <div> for example
# using just page_soup.div will only give the first one div tag

# The headtext of the article in VOA Burmese website is in <div> so extract that
headtext_container = page_soup.findAll("div", {"class": "col-title col-xs-12 col-md-10 pull-right"})

# In case there's no matched item, then exit!
if headtext_container == [] or isinstance(headtext_container,NoneType):
    print("There's no item in headtext_container")
    sys.exit()
else:
    # add the scraped text into final extracted content
    for headtext in headtext_container:
        h_text = str(headtext.find("h1").text)
        # print(h_text)
        extracted_content.append(h_text)

# Voa has a burmese text date
# It's seperated from the rest of the rest of the body content
date_container = page_soup.findAll("div", {"class": "published"})

if date_container == [] or isinstance(date_container,NoneType):
    print("There's no item in date_container")
    sys.exit()
else:
    for date in date_container:
        bur_date = str(date.span.time.text)
        # print(bur_date)
        dates.append(bur_date)

content_container = page_soup.find("div", {"class": "wsw"}) 

[s.extract() for s in content_container('blockquote')]
[s.extract() for s in content_container('script')]

if content_container == []:
    print("There's no item in the content_container")
    sys.exit()  # Alternative : if not date_container: works too
else:
    # print(content_container)

    #[s.extract() for s in content_container('br')]

    content_container = content_container.find_all("p")

    for content in content_container:
        text = str(content.text)
        # print(text)
        extracted_content.append(text)    

for entry in extracted_content:
    if entry == None:
        pass
    else:
        final_content.append(entry)


rows = final_content
del final_content[-1]

with open("C:\myanmar-website-crawlers\\voa_data.csv", "w", encoding='utf-8') as WR:
    writer = csv.writer(WR)
    for row in rows:
        writer.writerow([row])  # Need to add [] for item because without it,
        # the writer function will store each charaters and syllables as a column

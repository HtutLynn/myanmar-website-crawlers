import bs4
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from fake_useragent import UserAgent
import csv
import sys

ua = UserAgent()
headers = {'User-Agent': str(ua.random)}

# Put the desired url or website into the variable
# my_url = "http://www.mizzimaburmese.com/article/52168"
my_url = "http://mizzimaburmese.com/%25E1%2580%25A1%25E1%2580%2590%25E1%2580%25BD%25E1%2580%25B1%25E1%2580%25B8%25E1%2580%25A1%25E1%2580%2599%25E1%2580%25BC%25E1%2580%2584%25E1%2580%25BA-%25E1%2580%2586%25E1%2580%25B1%25E1%2580%25AC%25E1%2580%2584%25E1%2580%25BA%25E1%2580%25B8%25E1%2580%2595%25E1%2580%25AB%25E1%2580%25B8/article/137"
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

# Extract the Headtext from the tag
# And dump the information into the headtext_container
headtext_container = page_soup.findAll("div", {"class": "news-details-title"})

# In case there's no item in the headtext_container
if headtext_container == []:
    print("There is no item in teh bodytext_container")
    sys.exit()  # break only works within loop so we need to use sys.exit() instead
else:
    headtext = headtext_container[0].text

    # print(str(headtext))
    # append the headtext into extracted_content
    extracted_content.append(str(headtext))

# Extract the main article from the tag
# And dump the information into the bodytext_container
content_container = page_soup.find("div", {"class": "field-item even"}, {"property": "content:encoded"})

# In case there's  no matched item, then exit!
if content_container == []:
    print("There is no item in the bodytext_container")
    sys.exit()
else:
    [s.extract() for s in content_container('div')]
    [s.extract() for s in content_container('blockquote')]
    [s.extract() for s in content_container('script')]
    [s.extract() for s in content_container('img')]

    #[s.extract() for s in content_container('br')]

    content_container = content_container.find_all(
        "p", {"class": None})

    # Scenario One
    # All of main body content of the articles in mmtimes are witin a single <p> tag
    # Seperated by two <br /> tags between sentences so we can use find_all function for selecting text data
    # Instead we use childGenerator which generates characters on by one if they are different data structures
    # In this case, text are bs4.navigableStrings and <br /> are bs4.tag so
    # I use childGenerator to be able to get seperate texts as a single data and delete the tags

    # Scenario Two
    # Sometimes mmtimes write codes in the opposite way if scenario one
    # other sites are consistant with one sentence under one tag
    # mmtimes sometimes uses one sentence per one tag
    # or sometimes 3 sentences per tag or 2 per tag
    # That's why we needs to check if there are other children under each tag resulted from find_all
    # The method is combination of other websites + scenario one

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
                
    # deleting the None type empty content in finalized list which is about to write
    final_content = list(filter(None,final_content))

    del final_content[-1]

    with open("C:\myanmar-website-crawlers\Mizzima_data.csv", "w", encoding='utf-8') as WR:
        writer = csv.writer(WR)
        for item in final_content:
            # Need to add [] for item because without it,
            writer.writerow([item])
            # the writer function will store each charaters and syllables as a column
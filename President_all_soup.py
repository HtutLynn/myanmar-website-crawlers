import bs4
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from fake_useragent import UserAgent
import csv
import sys
import time
import pandas as pd
import numpy as np

ua = UserAgent()
headers = {'User-Agent': str(ua.random)}

urls = pd.read_csv("C:\myanmar-website-crawlers\President.csv", header=None)
urls = np.array(urls)
urls = urls.tolist()

NoneType = type(None) # for 'NoneTpye' specific error avoidance

wlist = []
for url in urls:
    #reconsructing urls from lists

    url = str(url).replace("[","").replace("'","").replace("]","")

    # can be change randint range between 1000 to 8000
    # 9000 is not stable
    try:
        print("Processing {}".format(url))
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
        req = Request(url, headers=headers)

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

        # The headtext of the article in mmtimes website is in <div> so extract that
        headtext_container = page_soup.findAll(
            "div", {"class": "news-detail-title"})

        # In case there's no matched item, then exit!
        if headtext_container == [] or isinstance(headtext_container, NoneType):
            print("There's no item in headtext_container")
            # sys.exit()
        else:
            # add the scraped text into final extracted content
            for headtext in headtext_container:
                extracted_content.append(str(headtext.text))

        # mmtimes has a special content called summary and
        # It's seperated from the rest of the rest of the body content
        summary_container = page_soup.findAll("div", {"class": "summary"})

        if summary_container == [] or isinstance(summary_container, NoneType):
            print("There's no item in summary_container")
            # sys.exit()
        else:
            for summary in summary_container:
                extracted_content.append(str(summary.text))

            content_container = page_soup.find(
                "div", {"class": "field-item even"})

        if content_container == [] or isinstance(content_container, NoneType):
            print("There's no item in the content_container")
            # sys.exit()  # Alternative : if not date_container: works too
        else:
            [s.extract() for s in content_container('div')]
            [s.extract() for s in content_container('blockquote')]
            [s.extract() for s in content_container('script')]

            #[s.extract() for s in content_container('br')]
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

            with open("C:\myanmar-website-crawlers\President_all_data.csv", "a", encoding='utf-8') as WR:
                writer = csv.writer(WR)
                for item in final_content:
                    # Need to add [] for item because without it,
                    writer.writerow([item])
                    # the writer function will store each charaters and syllables as a column
        time.sleep(10)
    except:
        print("There was an error while accessing this page")
        continue
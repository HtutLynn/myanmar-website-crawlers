import bs4
import time
import random
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from fake_useragent import UserAgent
import csv
import sys
import pandas as pd
import numpy as np
from random import shuffle

ua = UserAgent()
headers = {'User-Agent': str(ua.random)}

NoneType = type(None)  # for 'NoneTpye' specific error avoidance

urls = pd.read_csv("C:\myanmar-website-crawlers\\voa_urls_new.csv", header=None)
urls = np.array(urls)
urls = urls.tolist()
shuffle(urls)

page_counter = 0

for i in range(0,2376):
    # can be change randint range between 1000 to 8000
    # 9000 is not stable
    try:
        my_url = str(urls[i])

        my_url = my_url.replace("'","").replace("[","").replace("]","")

        page_counter +=1


        print(my_url)

        print("current page count %r" % (page_counter))

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
            # sys.exit()
        else:
            # add the scraped text into final extracted content
            for headtext in headtext_container:
                h_text = str(headtext.find("h1").text)
                # print(h_text)
            extracted_content.append(h_text)

        # All main paragraphs are in the div tag named 'wsw'
        # after getting the div, extract the text by p tag

        content_container = page_soup.find("div", {"class": "wsw"})

        [s.extract() for s in content_container('blockquote')]
        [s.extract() for s in content_container('script')]

        if content_container == []:
            print("There's no item in the content_container")
                # sys.exit()  # Alternative : if not date_container: works too
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
            del final_content[-2]

            with open("C:\myanmar-website-crawlers\\voa_all_data.csv", "a", encoding='utf-8') as WR:
                writer = csv.writer(WR)
                for item in final_content:
                    # Need to add [] for item because without it,
                    writer.writerow([item])
                    # the writer function will store each charaters and syllables as a column
        time.sleep(10)
    except:
        print("There was an error while accessing this page")
        continue

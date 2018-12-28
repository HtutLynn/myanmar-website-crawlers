import bs4
import time
import random
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from fake_useragent import UserAgent
import csv
import sys

ua = UserAgent()
headers = {'User-Agent': str(ua.random)}

NoneType = type(None) # for 'NoneTpye' specific error avoidance

#url_format = "http://mizzimaburmese.com" # for concatenation

year=2011

page_counter = 0

for i in range(0,2130,30):

    try:

        # pre-build a free container for extracted urls
        urls = []
        # pre-build a free container for titles
        titles = []
        # pre-build a free container for date
        
         # Put the desired url or website into the variable
        # News
        my_url = "https://www.rfa.org/burmese/news/story_archive?b_start:int="+str(i)+"&year="+ str(year)

        page_counter += 1

        print("Current page count %r " %(page_counter))

        print(my_url)
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

        # This time, the main target for scraping is href urls
        # urls are to be extracted from Eleven indexing page for each category
        # All articles are inside a similar named div tag
        # Extract all articles urls and their titles

        articles_container = page_soup.findAll("div", {"class" : "sectionteaser"})

        if articles_container == [] or isinstance(articles_container,NoneType):
            print("There's no urls or item in the container")
            continue
        else:

            for article in articles_container:
                article_url =str(article.h2.a['href'])
                article_title = article.h2.a.span.text

                urls.append(article_url)
                titles.append(article_title)
        
        # print(urls)
        rows = zip(urls,titles)

        with open("C:\myanmar-website-crawlers\\rfa_urls_news_2011.csv", "a", encoding='utf-8') as WR:
            writer = csv.writer(WR)
            for row in rows:
                # Need to add [] for item because without it,
                writer.writerow(row)
                # the writer function will store each charaters and syllables as a column
        time.sleep(5)
    except:
        print("There was an error while accessing this page")
        continue

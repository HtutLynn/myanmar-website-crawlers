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

url_format = "http://mizzimaburmese.com" # for concatenation



page_counter = 0

for i in range(0,8):

    try:
        
        # pre-build a free container for extracted urls
        urls = []
        # pre-build a free container for titles
        titles = []
        # pre-build a free container for date

         # Put the desired url or website into the variable
        # my_url = "http://mizzimaburmese.com/news/local?page="+str(i)
        my_url = "http://mizzimaburmese.com/business/international?page="+str(i)

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
        # urls are to be extracted from mizzima indexing page for each category
        # Main featured article is in the seperate div from other articles
        # Extract title and url from featured article div tag

        featured_article = page_soup.find("div", {"class": "news-category-large-image-title"})

        if featured_article == [] or isinstance(featured_article,NoneType):
            print("There's no url or item in the container")
            continue
        else:
            f_article_url = url_format + str(featured_article.a['href'])
            print(f_article_url)
            f_article_title   = featured_article.a.text
            urls.append(f_article_url)
            titles.append(f_article_title)

        # Extract the remaining article from the index pages
        # All articles are inside a similar named div tag
        # Extract all articles urls and their titles

        articles_container = page_soup.findAll("div", {"class" : "news-category-small-image-title"})

        if articles_container == [] or isinstance(articles_container,NoneType):
            print("There's no urls or item in the container")
            continue
        else:

            for article in articles_container:
                article_url = url_format + str(article.a['href'])
                article_title = article.a.text

                # append to respective lists after getting urls and titles
                if not article_url:
                    pass
                else:
                    urls.append(article_url)
                    titles.append(article_title)
        
        # print(urls)
        rows = zip(urls,titles)

        with open("C:\myanmar-website-crawlers\mizzima_urls_Economics.csv", "a", encoding='utf-8') as WR:
            writer = csv.writer(WR)
            for row in rows:
                # Need to add [] for item because without it,
                writer.writerow(row)
                # the writer function will store each charaters and syllables as a column
        time.sleep(30)
    except:
        print("There was an error while accessing this page")
        continue

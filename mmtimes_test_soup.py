import bs4
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
# from fake_useragent import UserAgent
import csv
import sys

my_url = "https://myanmar.mmtimes.com/news/118691.html"

req = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})

# save the html file into a container : page_html
page_html = urlopen(req).read()

page_soup = soup(page_html, "html.parser")

print(page_soup)
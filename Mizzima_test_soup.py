import bs4
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import csv
import sys

# Put the desired url or website into the variable
my_url = "http://www.mizzimaburmese.com/article/52168"

# pre-build a free list for final extracted content
extracted_content = []

# because of mod_security or some similar server security feature
# which blocks known spider/bot user agents (urllib uses something like python urllib/3.3.0,
# it's easily detected)
# So, We are gonna try it by sending a formal request
# with known browser agent in this case Mozilla
# If you send numerous request to server using just crawler and this ip-address
# It can get you banned so take care!

req = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})

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

# Extract the date from the tag
# And dump the information into date_container
date_container = page_soup.findAll("span", {"class": "date-display-single"})

# In case there is no matched item, then exit!
if date_container == []:
    print("There's no item in the soup_container")
    sys.exit() # Alternative : if not date_container: works too

# For accessing the date within the soup data structure, we need use index beacuse
# Sometimes it can have multiple values
date = date_container[0].text

# Extract the type of news from the tag
# # And dump the information into type_container


# Extract the Headtext from the tag
# And dump the information into the headtext_container
headtext_container = page_soup.findAll("div", {"class":"news-details-title"})

# In case there's no item in the headtext_container
if headtext_container == []:
    print("There is no item in teh bodytext_container")
    sys.exit() # break only works within loop so we need to use sys.exit() instead

headtext = headtext_container[0].text

#print(str(headtext))
# append the headtext into extracted_content
extracted_content.append(str(headtext))

# Extract the main article from the tag
# And dump the information into the bodytext_container
bodytext_container = page_soup.find("div", {"class" : "field-item even"} , {"property" : "content:encoded"})

# In case there's  no matched item, then exit!
if bodytext_container == []:
    print("There is no item in the bodytext_container")
    sys.exit()

# one <p> tag in the div is not the text we want so we need to ignore it
# We need to ignore <script> + <div> : Google ads tag in soup
[s.extract() for s in bodytext_container('script')]
[s.extract() for s in bodytext_container('div')]

bodytext_container = bodytext_container.find_all("p", {"class":None})

# And save the information into extracted_content by loop
for body in bodytext_container:
    extracted_content.append(str(body.text))

# append the date into final extracted content
extracted_content.append(str(date))

# Write the extracted content into csv file
with open("/Users/htutlinaung/Desktop/OCR/Mizzima_data.csv" , "w", encoding='utf-8') as WR:
    writer = csv.writer(WR)
    for item in extracted_content:
        writer.writerow([item]) # Need to add [] for item because without it,
                                # writer will store each charaters and syllables as a column
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

pd = 
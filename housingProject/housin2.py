import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import warnings
import selenium as se
import lxml
from lxml import html
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# from pyvirtualdisplay import Display
import time
import pikepdf

# from PyPDF2 import PdfFileReader
# import io
import PyPDF2
import urllib.request
from urllib.request import urlretrieve
from urllib.request import Request, urlopen 
import requests  

import slate3k as slate

with open('housing.pdf', 'rb') as f:
    doc = slate.PDF(f)[0]

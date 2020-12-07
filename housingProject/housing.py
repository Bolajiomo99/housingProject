import requests
from bs4 import BeautifulSoup

import json
from selenium import webdriver
import warnings
import selenium as se
import lxml
from lxml import html
import xlwt 
from xlwt import Workbook 
import csv

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import time
import re
from tika import parser
from PyPDF2 import PdfFileReader
import io
import PyPDF2
import urllib.request
# import urllib
import pikepdf
from selenium.webdriver.common.keys import Keys
# import bs4 as bs



with open('datatext') as filein:
    lines=filein.readlines()
    lines_sanitized = [line.strip() for line in lines if line != '\n' ]



codes = []
for line in lines_sanitized:
    if ',' in line and '.' in line:
        
        code = line.split()[:-1]
        strcode = ''.join(code)
        codes.append(strcode)


driver = webdriver.Chrome('chromedriver')
full_data= []
def get_data(html_data):
    soup = BeautifulSoup(html_data, "lxml")

    if soup.find('table', attrs={"id":"searchResults"}):
        number_results = len(soup.find_all('tr',attrs={'class':'SearchResults'}))
        print(number_results)
        for i in range(3,number_results+3):
            result_button = driver.find_element_by_xpath(f'//*[@id="searchResults"]/tbody/tr[{i}]')
            result_button.click()
            new_html_data = driver.page_source
            get_data(new_html_data)
            driver.back()
        return


    try:
        parcel_info = soup.find('table', attrs={"id":"Parcel"}).find_all("tr")
        data_dict = {}
        for row in parcel_info:
            row_data =row.find_all('td')
            if len(row_data) == 2:
                key = row_data[0].find(text=True)
                value = row_data[1].find(text=True)
                
                if value == "\u00a0":
                    value = None

                # print(key,value,sep=":")
                if key != "\u00a0":
                    if (key == 'Homestead /Farmstead' or key == 'Approved?') and value == '-':
                        value = "No"
                    
                    if key == 'Property Location':
                        if ' -' in value:
                            temp = value.replace(' -','-')
                            value = temp
                        value = re.sub(' +', ' ',value)
                    data_dict[key] = value


        get_Img('//*[@id="sidemenu"]/li[12]/a')
        


        print(json.dumps(data_dict, indent=4))        
        full_data.append(data_dict)
        # print(json.dumps(data_dict, indent=4))
            
        parcel_owner_details = soup.find('table',attrs={"id":"Parcel Mailing Address"}).find_all("tr")
        parcel_owner_alt_details = soup.find('table',attrs={"id":"Alternate Address"}).find_all("tr") 
        parcel_owner_ACT_flags = soup.find('table',attrs={"id":"ACT Flags"}).find_all("tr") 
        parcel_owner_tax_collector = soup.find('table',attrs={"id":"Tax Collector"}).find_all("tr") 
        parcel_assessor = soup.find('table',attrs={"id":"Assessor"}).find_all("tr")
    except:
        print('DAMNIT YUENG JOHN')
        
def get_Img(img):
    photo_button = driver.find_element_by_xpath(img)
    photo_button.click()
    time.sleep(3)

    


def search_Parcel(code):
    parcel_url = 'https://www.ncpub.org/_web/Search/Disclaimer.aspx?FromUrl=../search/commonsearch.aspx?mode=parid'
    driver.get(parcel_url)


    discosure_accept_button = driver.find_element_by_xpath('//*[@id="btAgree"]')
    discosure_accept_button.click()

    parcel_id_input_box = driver.find_element_by_xpath('//*[@id="inpParid"]')
    parcel_id_input_box.send_keys(code)

    submit_button = driver.find_element_by_xpath('//*[@id="btSearch"]')
    submit_button.click()
    html_data = driver.page_source

    
    get_data(html_data)


for code in codes:
    search_Parcel(code)
  


with open('webscrape.json', 'w') as out:
    out.write(json.dumps(full_data, indent=4))

print(full_data)
with open('webscrape.csv', 'w') as csvfile:
    csv_columns = list(full_data[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in full_data:
        writer.writerow(data)
driver.close()
from tika import parser
from helpers.filewriters import write_to_csv, write_to_json
from PyPDF2 import PdfFileReader
import io
import PyPDF2
import urllib.request
import pikepdf
import lxml
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import re
import time 
import csv
import traceback
# from helpers.filewriters import write_to_json, write_to_csv

# fileToRead='./housing.pdf'

# pdf = pikepdf.open(fileToRead)
# pdf.save('realestate.pdf')

# # file = open(fileToRead, 'rb')
# realestate = './realestate.pdf'

# raw = parser.from_file(realestate)
# print(raw['content'])


# with open('datatext', 'w') as f:
#     f.write(raw['content'])

with open('datatext') as filein:
    lines=filein.readlines()
    lines_sanitized = [line.strip() for line in lines if line != '\n' ]



codes = []
for line in lines_sanitized:
    if ',' in line and '.' in line:
        
        code = line.split()[:-1]
        strcode = ''.join(code)
        codes.append(strcode)


options = Options()
# options.headless = True

driver = webdriver.Chrome('chromedriver', options=options)
full_data = []

def get_data(code,html_data,child=False):
    data_dict = {}
    soup = BeautifulSoup(html_data, "lxml")
    child_scrape = False
    if soup.find('table', attrs={"id":"searchResults"}):

        number_results = len(soup.find_all('tr',attrs={'class':'SearchResults'}))
        print('TTHIS IS RIGHT BEFORE NUMBER RESULTS OR IS NUMBER RESULTS')
        print(number_results)
        for i in range(3,number_results+3):
            result_button = driver.find_element_by_xpath(f'//*[@id="searchResults"]/tbody/tr[{i}]')
            result_button.click()
            new_html_data = driver.page_source
            get_data(new_html_data,child=True)
            driver.back()

        return

    # image gallery
    # if 'Photos' in driver.title:
    #     delay = 3 # seconds
       
    #     myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH  , '//*[@id="image0"]')))
    #     imgsoup = BeautifulSoup(driver.page_source, "lxml")
    #     images_data = imgsoup.find_all('img')
    #     image_url_list = []
    #     for image2 in images_data:
    #         img_url_part = image2['src']
    #         if 'thumbnail' in img_url_part:
    #             image_url_full = 'https://www.ncpub.org/_web' + img_url_part[2:]
    #             large_image_url = image_url_full.replace('thumbnail','standard')
    #             print(large_image_url)
    #             image_url_list.append(large_image_url)

    #     data_dict['Photo_Urls'] = image_url_list
       

    try:
        data_dict['Parcel ID'] = code
        parcel_info = soup.find('table', attrs={"id":"Parcel"}).find_all("tr")
        
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
        
        get_value(data_dict)
        get_tax(data_dict)
        get_owner(data_dict)
        

        images_button = driver.find_element_by_xpath('//*[@id="sidemenu"]/li[12]/a')
        images_button.click()
            # image gallery
        if 'Photos' in driver.title:
            delay = 3 # seconds
            try:
                myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH  , '//*[@id="image0"]')))
                image_html = driver.page_source
                imgsoup = BeautifulSoup(driver.page_source, "lxml")
                images_data = imgsoup.find_all('img')
                image_url_list = []
                for image2 in images_data:
                    try:
                        img_url_part = image2['src']
                        if 'thumbnail' in img_url_part:
                            image_url_full = 'https://www.ncpub.org/_web' + img_url_part[2:]
                            large_image_url = image_url_full.replace('thumbnail','standard')
                            print(large_image_url)

                            image_url_list.append(large_image_url)
                    except Exception as er: 
                        traceback.print_tb(er.__traceback__)
                        data_dict['Photo_Urls'] = image_url_list

                data_dict['Photo_Urls'] = image_url_list
            except TimeoutException:
                pass
            if child:
                driver.back()
        
        print(json.dumps(data_dict, indent=4))

        full_data.append(data_dict)
        # print(json.dumps(data_dict, indent=4))
            
        # parcel_owner_details = soup.find('table',attrs={"id":"Parcel Mailing Address"}).find_all("tr")
        # parcel_owner_alt_details = soup.find('table',attrs={"id":"Alternate Address"}).find_all("tr") 
        # parcel_owner_ACT_flags = soup.find('table',attrs={"id":"ACT Flags"}).find_all("tr") 
        # parcel_owner_tax_collector = soup.find('table',attrs={"id":"Tax Collector"}).find_all("tr") 
        # parcel_assessor = soup.find('table',attrs={"id":"Assessor"}).find_all("tr")


    except Exception as err:
        traceback.print_tb(err.__traceback__)
        print('damnit yeunjohn!')

def get_tax(data_dict):

    tax_button = driver.find_element_by_xpath('//*[@id="sidemenu"]/li[11]/a')
    tax_button.click()
    html_data = driver.page_source
    time.sleep(0.5)
    soup = BeautifulSoup(html_data,"lxml")
    tax_data =  soup.find('table', id="Estimated Tax Information").find_all("tr")
    print('Tax Data RIGHT HERE!')
    for row in tax_data:
        tax_row_data = row.find_all('td')
        if len(tax_row_data) ==2:
            key = tax_row_data[0].find(text=True)
            value = tax_row_data[1].find(text=True)
            data_dict[key]=value


def get_owner(data_dict):
    owner_button = driver.find_element_by_xpath('//*[@id="sidemenu"]/li[2]/a')
    owner_button.click()
    html_data = driver.page_source
    # time.sleep(1)
    soup = BeautifulSoup(html_data, "lxml")
    owner_data = soup.find('table', id="Current Owner Details").find_all("tr")
    # print('Each line in owner data')
    for row in owner_data:
        owner_row_data = row.find_all('td')
        if len(owner_row_data) == 2:
            key = owner_row_data[0].find(text=True)
            value = owner_row_data[1].find(text=True)
            if key == '':
                continue
            if key=='Name(s)':
                key='Owner Name'
            data_dict[key] = value
            


def get_value(data_dict):
    value_button = driver.find_element_by_xpath('//*[@id="sidemenu"]/li[8]/a')
    value_button.click()
    html_data = driver.page_source
    # time.sleep(1)
    soup = BeautifulSoup(html_data, "lxml")
    value_data = soup.find('table', id="Values").find_all('tr')
    print('EACH LINE IN VALUE')
    for row in value_data:
        value_row_data = row.find_all('td')
        if len(value_row_data) ==2:
            key = value_row_data[0].find(text=True)
            value = value_row_data[1].find(text=True)
            data_dict[key] = value
            # print(key,value, sep= ' | ')

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

    
    get_data(code,html_data)



def write_to_json(full_data, loc):
    with open(loc, 'w') as out:
        out.write(json.dumps(full_data, indent=4))

def write_to_csv(full_data,loc):
    with open(loc, 'w') as csvfile:
        csv_columns = list(full_data[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for parcel in full_data:
            writer.writerow(parcel)




for code in codes:
    try:
        search_Parcel(code)
        print('parcel code is: ',code)
    except Exception as error:
        traceback.print_tb(error.__traceback__)
        print('Second yeunjohn!')

write_to_json(full_data, 'data.json')
write_to_csv(full_data, 'data.csv')



driver.close()
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import warnings
import selenium as se
import lxml
from lxml import html
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import time


from PyPDF2 import PdfFileReader
import io
import PyPDF2
import urllib.request
# import urllib


url=requests.get('https://www.northamptoncounty.org/FISAFF/REVENUE/Pages/UpsetSale.aspx')
soup = BeautifulSoup(url.content,"lxml")
pdfList = []
for a in soup.find_all('a', href=True):
    mystr= a['href']
    #print(mystr)
    if(mystr[-4:]=='.pdf'):
        # print ("url with pdf final:", a['href'])
        urlpdf = a['href']
        pdfList.append(urlpdf)
        # print(pdfList)
        # print(response)
response = requests.get('https://www.northamptoncounty.org'+pdfList[-1])
print(response)


wFile = urllib.request.urlopen('https://www.northamptoncounty.org'+pdfList[-1])
lFile = PyPDF2.pdf.PdfFileReader( cStringIO.StringIO(wFile.read()) )


# if response.isEncrypted:
#     response.decrypt('')
# input = pyPdf.PdfFileReader(<your file>)



# with io.BytesIO(response.content) as f:
#     pdf = PdfFileReader(f)


    
#     information = pdf.getDocumentInfo()
#     number_of_pages = pdf.getNumPages()
#     txt = f"""
#     Author: {information.author}
#     Creator: {information.creator}
#     Producer: {information.producer}
#     Subject: {information.subject}
#     Title: {information.title}
#     Number of pages: {number_of_pages}
#     """
#     # Here the metadata of your pdf
#     print(txt)
#     # numpage for the number page
#     numpage=20
#     page = pdf.getPage(numpage)
#     page_content = page.extractText()
#     # print the content in the page 20            
#     print(page_content)



















def realestate(search):
    url = f'https://liquipedia.net/{esport}'
    home= 'https://liquipedia.net'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    upcoming_matches = soup.find_all(class_='table table-striped infobox_matches_content')
    upcoming=False
    count=0
    matchups = []


def realtor(search):
    q = '%20'.join(search.split())
    display = Display(visible=0, size=(800, 800))  
    display.start()
    
    browser = webdriver.Chrome()
    browser.execute_script("window.navigator.geolocation.getCurrentPosition=function(success){"+
                                        "var position = {\"coords\" : {\"latitude\": \"33.735021\",\"longitude\": \"-112.181337\"}};"+
                                        "success(position);}")
    
    url = "https://www.totalwine.com/search/all?text="+ q
    browser.get(url) #navigate to the page
    time.sleep(1)
    innerHTML = browser.find_elements_by_class_name("grid__1eZnNfL-")
    # innerHTML = browser.get_attribute("innerHTML")
    toreturn = []
    for element in innerHTML:
        b = element.text.split('\n')
        
        for i in range(len(b)):
            print (b[i])

            # toreturn.append(b[i])
            if b[i] != '90' and b[i] !='Pick Up In Stock' and b[i] != 'Delivery Unavailable' and b[i] != 'Add to Cart':
                toreturn.append(b[i])
            if len(toreturn)>=5:
                break
    return toreturn
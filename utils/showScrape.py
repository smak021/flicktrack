import json
import re
from bs4 import BeautifulSoup
import requests
import cloudscraper
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
URL='https://in.bookmyshow.com/kozhikode/cinemas/aashirvad-cineplexx-kozhikode/AVCK/20221004'
scrapper = cloudscraper.create_scraper()
query = scrapper.get(URL)
soup = BeautifulSoup(query.content,"html.parser")
ssid = soup.find(string=re.compile("intAvgRating"))
js = ssid.rsplit('JSON.parse')[1].rsplit('");')[0].replace('("',"").rstrip().replace('\\',"")
dictt = json.loads(js)
print(js)
# for item in dictt['ShowDetails'][0]['Event']:
#     print(item['ChildEvents'][0]['EventName'])
#     print(dictt['ShowDetails'][0]['Event'][0]['ChildEvents'][0]['EventName'])


# URL2 = 'https://in.bookmyshow.com/booktickets/AVCK/64236'
# scrapper = cloudscraper.create_scraper()
# query = scrapper.get(URL2)
# soup = BeautifulSoup(query.content,"html.parser")
# ssid = soup.find_all(string=re.compile("EventCode"))
# for item in ssid:
#     js = item.rsplit('JSON.parse')[1].rsplit('function callSeatLayout')[0].replace('("',"").replace('");',"").rstrip().replace('\\',"")
#     dictt = json.loads(js)
#     print(js)


# options = Options()
# options.add_argument('--headless')
# driver = webdriver.Firefox(options=options,executable_path='utils/usr/bin/geckodriver.exe')

# driver.get(URL2)


# btn = driver.find_element(By.ID, "lnkMainBuyTickets").click()
# df  = driver.page_source
# ddf= WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "seat-layout")))
# # df = pd.read_html(driver.page_source)[0]
# data= driver.find_element(By.ID, "seat-layout")
# print(ddf)

# df.to_csv("data.csv", index=False)

# driver.quit()


# URL = 'https://in.bookmyshow.com/buytickets/ponniyin-selvan-part-1-kochi/movie-koch-ET00323897-MT/20221003#!seatlayout'
# URL = 'https://in.bookmyshow.com/buytickets/ponniyin-selvan-part-1-kochi/movie-koch-ET00323897-MT/20221003'
# print("Hello")
# element.click()

#     # tab = ssid.get('table')
#     print(item)
# # for item in ssid:

#    page = scrapper.get(website)
#         soup = BeautifulSoup(page.content, "html.parser")
#         ssid = soup.find_all('a',{'data-session-id':True,'data-venue-code':venue},class_='showtime-pill')
# section id> seat-layout  > table > td class=SRow1 > a._blocked or a._available
# _dc_gtm_UA-27207583-8

# /booktickets/CPCK/36079  %7Cmrs%3DCETA%3BCPCK%3BDSCC%3BEVMK%3B%7C

# Section id=seat-layout > div class=container > section -d=seatlayoutbox > div id=seatlayoutbox > div class=seat-container > div class=seats > div class=_block > div id=layout > table
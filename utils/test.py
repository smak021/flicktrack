from collections import OrderedDict
from ftplib import FTP_PORT
from os import sep
from telnetlib import TN3270E
from time import strptime
from unicodedata import category
from xml.sax.handler import feature_validation
import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import date
import pytz
from datetime import datetime, timedelta
from difflib import SequenceMatcher
import cloudscraper
import socket



# sub
# try:
#                 scrapper = cloudscraper.create_scraper()
#                 url2 = scrapper.get(website2).text
#                 data = json.loads(url2)
#             except:
#                 print("Error reading main data")
#             else:
#                 for urll in data['BookMyShow']['arrShowInfo']:
#                     tot_seat = int(urll['TotalSeats'])
#                     avail_seat = int(urll['AvailableSeats'])
#                     total_seat+=int(urll['TotalSeats'])
#                     offset_in = 0
#                     if(offset!='na'):
#                         ind_offset = offset.rsplit('],')
#                         for roffset in ind_offset:
#                             offset_splt = roffset.rsplit(':[')
#                             if(offset_splt[0]==urll['ScreenName']):
#                                 for item2 in offset_splt[1].replace(']',"").rsplit(','):
#                                     fin_split = item2.rsplit(':')
#                                     if(fin_split[0]==urll['CategoryName']):
#                                         offset_in = int(fin_split[1])
            
#                     print("Offset:",offset_in)
#                     if(tot_seat-avail_seat < offset_in):
#                         offset_in = 0
#                     available_seat+= avail_seat + offset_in
#                     bm_show_date=urll['ShowDateCode']
#                     booked_seat += tot_seat-(avail_seat+offset_in)
#                     price = price + (float(urll['Price']) * (tot_seat-(avail_seat+offset_in)))
#                     category_name= category_name+urll['CategoryName']+":"
#                     print(category_name)
#                     screen_name = screen_name+urll['ScreenName']+ ":"
#                     Current_date = date.today()
#                     d1 = Current_date.strftime('%Y%m%d')






# wORKING API READ WITHOUT CLOUDSCRAPPER !iMPORTANT
answers = socket.getaddrinfo('in.bookmyshow.com', 443)
(family, type, proto, canonname, (address, port)) = answers[0]

s = requests.Session()
headers = OrderedDict({
    'Host': "in.bookmyshow.com",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
})
s.headers = headers
response = s.get(f"https://{address}/serv/getData?cmd=GETSHOWINFOJSON&vid=MCIK&ssid=9194&format=json", headers=headers, verify=False).text
print("H")
print(response)



# website2 = 'https://in.bookmyshow.com/serv/getData?cmd=GETSHOWINFOJSON&vid=MCIK&ssid=9194&format=json'
# scrapper = cloudscraper.create_scraper()
# url2 = scrapper.get(website2)
# print(url2.request.headers)
# print(url2.status_code)
# print(url2.text)
# data = json.loads(url2.text)
# print(type(data))


# scrapper = cloudscraper.create_scraper()
# website2 = 'https://in.bookmyshow.com/serv/getData?cmd=GETSHOWINFOJSON&vid=AVCK&ssid=64225&format=json'
# url2 = scrapper.get(website2).text
# data = json.loads(url2)
# print(data)

# total = 212
# offset = 27
# avail = 184
# bal = 0
# ft_st = 'FTADJST'
# ft_value = 212

# if(ft_st == 'FTADJST'):
#     bal = ft_value


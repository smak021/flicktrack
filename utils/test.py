from telnetlib import TN3270E
from time import strptime
import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import date
import pytz
from datetime import datetime, timedelta
from difflib import SequenceMatcher

# BMS Efficient


arr=['235','43432','4355']
test=''
for ser in [1,2]:
    for count,item in enumerate(arr,start=1):
        print(item)
    print(count)

# for n in arr:
#     test = ':'.join([n,test])
   
# print(test.rstrip(':'))


# Find date or time difference
def dateDiff(inputDate):
    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY)
    dateFormat = '%Y%m%d %I:%M %p'
    todaydate = datetime_NY.strftime(dateFormat)
    inDate = datetime.strptime(todaydate, dateFormat)
    tDate = datetime.strptime(inputDate, dateFormat)
    res = inDate - tDate
    return res

# res = dateDiff('20220905',None)
# print(res.days)
# print(res.seconds)
# tz_NY = pytz.timezone('Asia/Kolkata')   
# datetime_NY = datetime.now(tz_NY)
# print(datetime_NY.strftime('%I:%M %p'))
# def bms_track(theatre_code,location,loc_slug):
#     url = 'https://in.bookmyshow.com/'+loc_slug+'/cinemas'
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, "html.parser")
#     ssid = soup.find('a',attrs={'href':re.compile(theatre_code)})
#     print(ssid['href'])
#     theatre_url = "https://in.bookmyshow.com/"+loc_slug+ssid['href']
#     # print(theatre_url)
#     theatre_page = requests.get(theatre_url)
#     soup = BeautifulSoup(theatre_page.content, "html.parser")
#     ssid = soup.find_all('a',{'onclick':re.compile(theatre_code)})
#     for row in ssid:
#         print("------------------------------------------------------")
#         data = row['onclick'].rsplit('(')[1].replace(');','').replace("'","").rsplit(',')
#         # print(row['onclick'].rsplit('(')[1].replace(');','').replace("'","").rsplit(','))
#         session = data[1]
#         film_id = data[2]
#         show_time = data[3]
#         print("Show_id:", session)
#         print("Film_id:",film_id)
#         print("Show Time:",show_time)
#         venue_url=requests.get('https://in.bookmyshow.com/serv/getData?cmd=VENUESHOWCASE&venueCode='+theatre_code).text
#         vjson = json.loads(venue_url)
#         theatre_name = vjson['data']['venueName']
#         print(theatre_name)
#         film_url=requests.get('http://flicktracks.herokuapp.com/api/films/').text
#         fjson = json.loads(film_url)
#         ffilm_id = fjson
#         # print(ffilm_id)
#         print(film_id)
#         vard = [item for item in ffilm_id if item["film_id"] == film_id]
#         if(vard):
#             website2 = 'https://in.bookmyshow.com/serv/getData?cmd=GETSHOWINFOJSON&vid='+theatre_code+'&ssid='+session+'&format=json'
#             url2 = requests.get(website2).text
#             data = json.loads(url2)
#             for urll in data['BookMyShow']['arrShowInfo']:
#                 total_seat=int(urll['TotalSeats'])
#                 available_seat = int(urll['AvailableSeats'])
#                 show_date=urll['ShowDateCode']
#                 price = urll['Price']
#                 category_name= urll['CategoryName']
#                 print(category_name)
#                 screen_name = urll['ScreenName']
#                 booked_seat = int(total_seat)-int(available_seat)
#                 Current_date = date.today()
#                 d1 = Current_date.strftime('%Y%m%d')
#                 print(d1)
#                 print('Film ID:',theatre_code)
#                 print("Show ID",session)
#                 print('Show Time:',show_time)
#                 print('Show Date:',show_date)
#                 print('Total Seats:', total_seat)
#                 print('Price:', price)
#                 print('Available Seats:', available_seat)
#                 print('Booked Seats: ',booked_seat)
#                 # cur_time=datetime_NY.strftime('%I:%M %p')
#                 # cur_spt_time=timesplit(cur_time)
#                 # show_spt_time=timesplit(show_time)
#                 # add_cur_time=datetime.strptime(cur_time,'%I:%M %p') + timedelta(minutes=30)
#                 # new_cur_time=add_cur_time.strftime('%I:%M %p')
#                 # datta =  {"show_id": session,"theatre_name":theatre_name,"show_time": show_time,"screen_name": screen_name,"show_date": show_date,"category_name": category_name,"price": price,"booked_seats": booked_seat,"available_seats": available_seat,"total_seats": total_seat,"theatre_code": venue,"theatre_location": fm_loc,"last_modified": cur_time,"film": show_id}
            
            
    







# locData = requests.get('http://flicktracks.herokuapp.com/api/tracks/').text
# locData_json = json.loads(locData)
# for loc in locData_json:
#     bms_track(loc['theatre_code'],loc['track_location'],loc['loc_real_name'])

# film_data= requests.get('http://flicktracks.herokuapp.com/api/films/').text
# film_data_json = json.loads(film_data)
# locData = requests.get('http://flicktracks.herokuapp.com/api/tracks/').text
# locData_json = json.loads(locData)
# for film in film_data_json:
#     if(film['film_status']!='inactive' or film['film_status']!='stopped'):
#         for loc in locData_json:
#             if(loc['is_currently_tracking']!='no' or loc['is_currently_tracking']!='N') :
#                 bms()
#                 if(film['ptm_code']!='NA') and (loc['source']=='ptm'):
#                     paytm()
#                 if(film['tn_code']!='NA') and (loc['source']=='tn'):
#                     tn()
                
                


# city = 'kozhikode'
# website = 'https://paytm.com/movies/kozhikode/regal-cinema-c/2661'
# page = requests.get(website,cookies={'movies_city': city})
# soup = BeautifulSoup(page.content, "html.parser")
# # print(soup)
# ssid = soup.find_all('div',class_='MovieSessionsListing_timeblock__S_Z44')
# for time in ssid:
#     print(time.div.text)
#     print(time.div.text)






    


# tktnewUrl = "https://www.ticketnew.com/test/Online-Advance-Booking/25382/C/Mukkam/"
# requ = requests.get(tktnewUrl)
# venue_code = '15123'
# html = BeautifulSoup(requ.content,"html.parser")
# movie_name = html.find("div",class_='movie-details tn-entity-details')
# query = html.find_all("a",{'data-venue':True,'data-venue':venue_code})
# for val in query:
#     print(val.text)
#     date = val['data-date'].rsplit('-')
#     print(val['data-date'])
#     nw_date = date[0]+date[1]+date[2]
#     print(date)
#     print(nw_date)


# #BMS - Ticket New Linking by comparing
# bms_title = 'Liger (U/A)  -Malayalam'

# tktnew_title = "Liger (Malayalam)"

# check_match = SequenceMatcher(None,tktnew_title.lower(),bms_title.lower()).ratio()
# print(check_match)

# if check_match>0.8:
#     print("Matches")
# else:
#     print("No Match")

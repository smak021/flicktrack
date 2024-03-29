from datetime import datetime, timedelta
from unicodedata import category
import requests
import json
from datetime import date
from bs4 import BeautifulSoup
import pytz
# from api.views import mainData

def timesplit(time):
    tmwopm=time.rsplit(' ',1)[-2]
    tmhr=time.rsplit(':',1)[-2]
    tmmin=tmwopm.rsplit(':',1)[-1]
    tmampm=time.rsplit(' ',1)[-1]
    return [tmhr,tmmin,tmampm]


def main_data(film_namee,film_ID, fm_loc, loc_slug, venue):
    # uu= requests.get('http://flicktracks.herokuapp.com/api/tracks/').text
    # json_data=json.loads(uu)
    # for fmlo in json_data:
    #     if fmlo['track_location'] == fm_loc:
    #         loc_slug=fmlo['loc_real_name']
    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY)
    d1 = datetime_NY.strftime('%Y%m%d')
    website = 'https://in.bookmyshow.com/buytickets/'+film_namee+'-'+loc_slug+'/movie-'+fm_loc.lower()+'-'+film_ID+'-MT/'+d1
    try:
        page = requests.get(website)
        soup = BeautifulSoup(page.content, "html.parser")
        ssid = soup.find_all('a',{'data-session-id':True,'data-venue-code':venue},class_='showtime-pill')
    except :
        print("Error reading")
        ssid = False
    total_seat=0
    session = ''
    available_seat=0
    i=0    
    booked_seat=0
    price=0
    if(ssid):
        for values in ssid:
            i+=1
            session = values['data-session-id']
            venue = values['data-venue-code']
            show_time = values['data-display-showtime']
            show_id = values['data-event-id']
            venue_url=requests.get('https://in.bookmyshow.com/serv/getData?cmd=VENUESHOWCASE&venueCode='+venue).text
            vjson = json.loads(venue_url)
            theatre_name = vjson['data']['venueName']
            print("-------------------------------")
            print("Film_Name",film_namee)
            print("Theatre_Code:",venue)
            print("Show Count:",i)
            print("Show_id:",session)
            website2 = 'https://in.bookmyshow.com/serv/getData?cmd=GETSHOWINFOJSON&vid='+venue+'&ssid='+session+'&format=json'
            url2 = requests.get(website2).text
            data = json.loads(url2)
            for urll in data['BookMyShow']['arrShowInfo']:
                testtotal_seat=urll['TotalSeats']
                total_seat+=int(urll['TotalSeats'])
                available_seat+= int(urll['AvailableSeats'])
                show_date=urll['ShowDateCode']
                booked_seat += int(urll['TotalSeats'])-int(urll['AvailableSeats'])
                price = price + (float(urll['Price']) * (int(urll['TotalSeats'])-int(urll['AvailableSeats'])))
                category_name= urll['CategoryName']
                print(category_name)
                screen_name = urll['ScreenName']
                Current_date = date.today()
                d1 = Current_date.strftime('%Y%m%d')
                #print(d1)
                # print('Film ID:',show_id)
                # print("Show ID",session)
                # print('Show Time:',show_time)
                # print('Show Date:',show_date)
                # print('test Total Seats:',testtotal_seat)
                # print('Total Seats:', total_seat)
                # print('Price:', price)
                # print('Available Seats:', available_seat)
                # print('Booked Seats: ',booked_seat)
                cur_time=datetime_NY.strftime('%I:%M %p')
                cur_spt_time=timesplit(cur_time)
                show_spt_time=timesplit(show_time)
                add_cur_time=datetime.strptime(cur_time,'%I:%M %p') + timedelta(minutes=30)
                new_cur_time=add_cur_time.strftime('%I:%M %p')
        datta =  {"show_id": session,"shows":i,"theatre_name":theatre_name,"show_time": show_time,"screen_name": screen_name,"show_date": show_date,"category_name": category_name,"price": price,"booked_seats": booked_seat,"available_seats": available_seat,"total_seats": total_seat,"theatre_code": venue,"theatre_location": fm_loc,"last_modified": cur_time,"film": show_id}
        print(datta)
        
            # putt = requests.put('http://flicktracks.herokuapp.com/api/putshow/'+session+'/'+category_name+'/',json=datta, headers={'Content-type': 'application/json'})
            # print("Status Code:",putt.status_code)
           
            

film_data= requests.get('http://flicktracks.herokuapp.com/api/films/').text
film_data_json = json.loads(film_data)
locData = requests.get('http://flicktracks.herokuapp.com/api/tracks/').text
locData_json = json.loads(locData)
# print(locData_json)
for film in film_data_json:
    for loc in locData_json:
        main_data(film['film_name'], film['film_id'], loc['track_location'], loc['loc_real_name'],loc['theatre_code'])
            
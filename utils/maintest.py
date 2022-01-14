from datetime import datetime, timedelta
from email import header
import requests
import json
from datetime import date
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import pytz

def timesplit(time):
    tmwopm=time.rsplit(' ',1)[-2]
    tmhr=time.rsplit(':',1)[-2]
    tmmin=tmwopm.rsplit(':',1)[-1]
    tmampm=time.rsplit(' ',1)[-1]
    return [tmhr,tmmin,tmampm]


def main_data(film_namee,Sh_tm, fm_loc):
    uu= requests.get('http://127.0.0.1:8000/getlocdata/').text
    json_data=json.loads(uu)
    for fmlo in json_data:
        if fmlo['film_location'] == fm_loc:
            loc_slug=fmlo['venue_id']

    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY)
    d1 = datetime_NY.strftime('%Y%m%d')
    #for x in myresult:
    website = 'https://in.bookmyshow.com/buytickets/'+film_namee+'-'+loc_slug+'/movie-'+fm_loc.lower()+'-'+Sh_tm+'-MT/'+d1
    page = requests.get(website)
    soup = BeautifulSoup(page.content, "html.parser")
    ssid = soup.find_all('a',{'data-session-id':True},class_='showtime-pill')
    for values in ssid:
        session = values['data-session-id']
        venue = values['data-venue-code']
        show_time = values['data-display-showtime']
        show_id = values['data-event-id']
        print(film_namee)
        print(venue)
        print(session)
        website2 = 'https://in.bookmyshow.com/serv/getData?cmd=GETSHOWINFOJSON&vid='+venue+'&ssid='+session+'&format=json'
        url2 = requests.get(website2).text
        data = json.loads(url2)
        i=0
        total_seat=0
        available_seat=0
        booked_seat=0
            
        for urll in data['BookMyShow']['arrShowInfo']:
            total_seat=total_seat + int(urll['TotalSeats'])
            available_seat = available_seat + int(urll['AvailableSeats'])
            show_date=urll['ShowDateCode']
            price = urll['Price']
            
        booked_seat = int(total_seat)-int(available_seat)
        Current_date = date.today()
        d1 = Current_date.strftime('%Y%m%d')
        #print(d1)
        print('Show ID:',show_id)
        print('Show Time:',show_time)
        print('Show Date:',show_date)
        print('Total Seats:', total_seat)
        print('Price:', price)
        print('Available Seats:', available_seat)
        print('Booked Seats: ',booked_seat)
        cur_time=datetime_NY.strftime('%I:%M %p')
        cur_spt_time=timesplit(cur_time)
        show_spt_time=timesplit(show_time)
        add_cur_time=datetime.strptime(cur_time,'%I:%M %p') + timedelta(minutes=30)
        new_cur_time=add_cur_time.strftime('%I:%M %p')
        if cur_spt_time[2]==show_spt_time[2] and new_cur_time>show_time:
            pass
        else:
            
            filmdata={"film_name": film_namee, "film_id": show_id, "theatre_id": venue, "show_id": session, "available_seat": available_seat, "total_seat": total_seat, "booked_seat": booked_seat, "Show_time": show_time, "show_date": show_date, "price":price ,"film_loc":fm_loc , "last_modified": cur_time}
            filmdata_json = json.dumps(filmdata)
            r= requests.put('http://127.0.0.1:8000/gufilm/'+session+'/'+show_date+'/'+show_id+'/', json=filmdata, headers={'Content-type': 'application/json'})
            #r= requests.post('http://127.0.0.1:8000/getdata/', json=filmdata, headers={'Content-type': 'application/json'})
        

film_data= requests.get('http://127.0.0.1:8000/getfilmdata/').text
film_data_json = json.loads(film_data)
for un in film_data_json:
    print(un['film_name'])
    main_data(un['film_name'], un['film_id'], un['film_loc'])
            
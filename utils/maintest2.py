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

def currentTime():
    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY)
    cur_time=datetime_NY.strftime('%I:%M %p')
    return cur_time

def main_data(film_namee,film_ID, fm_loc,loc_slug, venue):
    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY)
    d1 = datetime_NY.strftime('%Y%m%d')
    website = 'https://in.bookmyshow.com/buytickets/'+film_namee+'-'+loc_slug+'/movie-'+fm_loc.lower()+'-'+film_ID+'-MT/'+d1
    page = requests.get(website)
    soup = BeautifulSoup(page.content, "html.parser")
    ssid = soup.find_all('a',{'data-session-id':True,'data-venue-code':venue},class_='showtime-pill')
    for values in ssid:
        session = values['data-session-id']
        # venue = values['data-venue-code']
        venue_url=requests.get('https://in.bookmyshow.com/serv/getData?cmd=VENUESHOWCASE&venueCode='+venue).text
        vjson = json.loads(venue_url)
        theatre_name = vjson['data']['venueName']
        show_time = values['data-display-showtime']
        show_id = values['data-event-id']
        print("-------------------------------")
        print(film_namee)
        print(venue)
        print(theatre_name)
        print(session)
        website2 = 'https://in.bookmyshow.com/serv/getData?cmd=GETSHOWINFOJSON&vid='+venue+'&ssid='+session+'&format=json'
        
        url2 = requests.get(website2).text
        data = json.loads(url2)
        i=0
        total_seat=0
        available_seat=0
        booked_seat=0
            
        for urll in data['BookMyShow']['arrShowInfo']:
            total_seat=int(urll['TotalSeats'])
            available_seat = int(urll['AvailableSeats'])
            show_date=urll['ShowDateCode']
            price = urll['Price']
            category_name= urll['CategoryName']
            print(category_name)
            screen_name = urll['ScreenName']
            booked_seat = int(total_seat)-int(available_seat)
            Current_date = date.today()
            d1 = Current_date.strftime('%Y%m%d')
            print(d1)
            print('Film ID:',show_id)
            print("Show ID",session)
            print('Show Time:',show_time)
            print('Show Date:',show_date)
            print('Total Seats:', total_seat)
            print('Price:', price)
            print('Available Seats:', available_seat)
            print('Booked Seats: ',booked_seat)
            cur_time=datetime_NY.strftime('%I:%M %p')
            # cur_spt_time=timesplit(cur_time)
            # show_spt_time=timesplit(show_time)
            # add_cur_time=datetime.strptime(cur_time,'%I:%M %p') + timedelta(minutes=30)
            # new_cur_time=add_cur_time.strftime('%I:%M %p')
            datta =  {"show_id": session,"theatre_name":theatre_name,"show_time": show_time,"screen_name": screen_name,"show_date": show_date,"category_name": category_name,"price": price,"booked_seats": booked_seat,"available_seats": available_seat,"total_seats": total_seat,"theatre_code": venue,"theatre_location": fm_loc,"last_modified": cur_time,"film": show_id}
            putt = requests.put('http://flicktracks.herokuapp.com/api/putshow/'+session+'/'+category_name+'/',json=datta, headers={'Content-type': 'application/json'})
            print("Status Code:",putt.status_code)
           
def ptm_track(code,ptm_theatre_id,city,bm_id,offset):
    url = "https://apiproxy.paytm.com/v3/movies/search/movie?meta=1&reqData=1&city="+city+"&movieCode="+code+"&version=3&site_id=1&channel=HTML5&child_site_id=1" 
    data = requests.get(url).text
    if(data):
        json_data = json.loads(data)
        # print("theatre:",json_data['meta']['cinemas'][0]['name'])
        # print(json_data['pageData']['sessions'])
        for row in json_data['pageData']['sessions']:
            for show in json_data['pageData']['sessions'][row]:
                cid = show['cid']
                if(cid == int(ptm_theatre_id)):
                    my_item = next((item for item in json_data['meta']['cinemas'] if item['id'] == cid), None)
                    print("Ptm ID",code)
                    print("film_id:",bm_id)
                    show_id = show['sid']
                    print("Show_id:", show_id)
                    theatre_name = my_item['name']
                    print("Theatre name:",theatre_name)
                    theatre_code = show['cid']
                    print("theatre code:", theatre_code)
                    print("theatre location:",city)
                    try:
                        screen_name = show['audi']
                        print("Screen: ",screen_name)
                    except KeyError:
                        screen_name='na'
                        print("not found")
                    date = show['showTime'].rsplit('T')[0].rsplit('-')
                    ptm_date = date[0]+date[1]+date[2]
                    print("Date:",ptm_date)
                    ptm_time = "ptm "+show['showTime'].rsplit('T')[1]
                    print("Time:",ptm_time)
                    for section in show['areas']:
                        category_name = section['label']
                        total_seat = section['sTotal']
                        if(offset!='na'):
                            offset_in = int(offset)
                        else:
                            offset_in = 0
                        available_seat = section['sAvail'] + offset_in
                        booked_seat = section['sTotal']-section['sAvail']
                        price = section['price']
                        print("Category Name:", category_name)
                        print("Total:",total_seat)
                        print("Available: ",available_seat)
                        print("Booked:",booked_seat)
                        print("Price",price)
                        cur_time=currentTime()
                        payload ={"show_id": show_id,"theatre_name":theatre_name,"show_time": ptm_time,"screen_name": screen_name,"show_date": ptm_date,"category_name": category_name,"price": price,"booked_seats": booked_seat,"available_seats": available_seat,"total_seats": total_seat,"theatre_code": theatre_code,"theatre_location": city,"last_modified": cur_time,"film": bm_id}
                        putt = requests.put('http://flicktracks.herokuapp.com/api/putshow/'+show_id+'/'+category_name+'/',json=payload, headers={'Content-type': 'application/json'})
                        print("Status Code:",putt.status_code)
                    print("------------------------------------------")           

# film_data= requests.get('http://flicktracks.herokuapp.com/api/films/').text
# film_data_json = json.loads(film_data)
# locData = requests.get('http://flicktracks.herokuapp.com/api/tracks/').text
# locData_json = json.loads(locData)
# # print(locData_json)
# for film in film_data_json:
#     for loc in locData_json:
#         main_data(film['film_name'], film['film_id'], loc['track_location'], loc['loc_real_name'])

# Test Call

film_data= requests.get('http://flicktracks.herokuapp.com/api/films/').text
film_data_json = json.loads(film_data)
locData = requests.get('http://flicktracks.herokuapp.com/api/tracks/').text
locData_json = json.loads(locData)
for film in film_data_json:
    if (film['film_status']!='inactive') or (film['film_status']!='stopped'):
        for loc in locData_json:
            if (loc['is_currently_tracking']!='no' or loc['is_currently_tracking']!='N'):
                if(loc['source']=='bms'):
                    main_data(film['film_name'],film['film_id'],loc['track_location'],loc['loc_real_name'],loc['theatre_code'])
                if(film['ptm_code']!='NA') and (loc['source']=='ptm'):
                    ptm_track(film['ptm_code'],loc['theatre_code'],loc['track_location'], film['film_id'],loc['offset'])

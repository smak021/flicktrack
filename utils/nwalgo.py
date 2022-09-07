from datetime import datetime, timedelta
from operator import le
from unicodedata import category
import requests
import json
from datetime import date
from bs4 import BeautifulSoup
import pytz
# from api.views import mainData

# bm
def dateDiff(inputDate):
    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY)
    dateFormat = '%Y%m%d %I:%M %p'
    todaydate = datetime_NY.strftime(dateFormat)
    inDate = datetime.strptime(todaydate, dateFormat)
    tDate = datetime.strptime(inputDate, dateFormat)
    res = inDate - tDate
    return res

def timesplit(time):
    tmwopm=time.rsplit(' ',1)[-2]
    tmhr=time.rsplit(':',1)[-2]
    tmmin=tmwopm.rsplit(':',1)[-1]
    tmampm=time.rsplit(' ',1)[-1]
    return [tmhr,tmmin,tmampm]

def new_algo_bm(film_namee,film_ID, fm_loc, loc_slug, venue):
    print("---------------------------------------------")
    print("Venue",venue)
    try:
        venue_url=requests.get('https://in.bookmyshow.com/serv/getData?cmd=VENUESHOWCASE&venueCode='+venue).text
        vjson = json.loads(venue_url)
        theatre_name = vjson['data']['venueName']
    except:
        theatre_name = venue
    print("Film: ",film_namee)
    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY)
    d1 = datetime_NY.strftime('%Y%m%d')
    print("Iteration Start")
    website = 'https://in.bookmyshow.com/buytickets/'+film_namee+'-'+loc_slug+'/movie-'+fm_loc.lower()+'-'+film_ID+'-MT/'+d1
    try:
        page = requests.get(website)
        soup = BeautifulSoup(page.content, "html.parser")
        ssid = soup.find_all('a',{'data-session-id':True,'data-venue-code':venue},class_='showtime-pill')
    except :
        print("Not found")
        ssid = False
    if(ssid):
        show_count =0 
        for values in ssid:
            show_count+=1
            session = values['data-session-id']
            venue = values['data-venue-code']
            show_date = values['data-cut-off-date-time'][0:8]
            show_time = values['data-display-showtime']
            film_id = values['data-event-id']
            print("ID:",session,'| Date:',show_date,"| Venue: ",venue,"| Show Time:",show_time,"| Film ID:",film_id,"| Theatre Name:",theatre_name)
            cur_time=datetime_NY.strftime('%d/%m/%Y %I:%M %p')  
            payload = {"show_id": session,"show_time": show_time,"show_date": show_date,"screen_name": "NA","theatre_code": venue,"last_modified": cur_time,"film": film_id}
            putShow = requests.put('http://flicktracks.herokuapp.com/api/putshow/'+session+'/',json=payload, headers={'Content-type': 'application/json'})
            print(putShow.status_code)

        print("Loop")
        total_seat=0
        available_seat=0  
        booked_seat=0
        price=0
        print(d1)
        show_url = requests.get('http://flicktracks.herokuapp.com/api/getshows/'+venue+'/'+d1+'/'+film_ID+'/')
        show_dict = json.loads(show_url.text)
        count = 0
        for count,show in enumerate(show_dict,start=1):
            print(show)
            print(show['show_id'])
            website2 = 'https://in.bookmyshow.com/serv/getData?cmd=GETSHOWINFOJSON&vid='+venue+'&ssid='+show['show_id']+'&format=json'
            url2 = requests.get(website2).text
            if(url2):
                screen_name =''
                category_name = ''
                data = json.loads(url2)
                for urll in data['BookMyShow']['arrShowInfo']:
                    total_seat+=int(urll['TotalSeats'])
                    available_seat+= int(urll['AvailableSeats'])
                    show_date=urll['ShowDateCode']
                    booked_seat += int(urll['TotalSeats'])-int(urll['AvailableSeats'])
                    price = price + (float(urll['Price']) * (int(urll['TotalSeats'])-int(urll['AvailableSeats'])))
                    category_name= category_name+urll['CategoryName']+":"
                    print(category_name)
                    screen_name = screen_name+urll['ScreenName']+ ":"
                    Current_date = date.today()
                    d1 = Current_date.strftime('%Y%m%d')
        cur_time=datetime_NY.strftime('%d/%m/%Y %I:%M %p')
        payload2 = {"show_date":show_date,"show_count":count,"film":film_ID,"theatre_code":venue,"theatre_location":fm_loc,"theatre_name":theatre_name,"category_name": category_name.rstrip(':'),"price": price,"booked_seats": booked_seat,"available_seats": available_seat,"total_seats": total_seat,"last_modified": cur_time}
        putData = requests.put('http://flicktracks.herokuapp.com/api/porgdata/'+venue+'/'+show_date+'/'+film_ID+'/',json=payload2, headers={'Content-type': 'application/json'})
        print(putData.status_code)
                 
# ptm

def new_algo_ptm(code,ptm_theatre_id,city,bm_id,offset):
    print("------------------------------------------")
    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY)
    print("Entered",city,code)
    url = "https://apiproxy.paytm.com/v3/movies/search/movie?meta=1&reqData=1&city="+city+"&movieCode="+code+"&version=3&site_id=1&channel=HTML5&child_site_id=1" 
    data = requests.get(url).text
    if(data):
        json_data = json.loads(data)
        show_count = 0 
        total_seats = 0
        available_seats = 0
        price = 0
        try:
            theatre = json_data['pageData']['sessions'][ptm_theatre_id]
        except:
            print("Show not found")
            theatre = []
        for row in theatre:
            show_count+=1
            date = row['showTime'].rsplit('T')[0].rsplit('-')
            ptm_date = date[0]+date[1]+date[2]
            theatre_code = row['cid']
            try:
                screen_name = row['audi']
                print("Screen: ",screen_name)
            except KeyError:
                screen_name='na'
                print("not found")
            print("Name:",json_data['meta']['movies'][0]['name'])
            my_item = next((item for item in json_data['meta']['cinemas'] if item['id'] == int(ptm_theatre_id)), None)
            theatre_name = my_item['name']
            print(theatre_name)
            for section in row['areas']:
                category_name = section['label']
                total_seat = section['sTotal']
                total_seats += total_seat
                if(offset!='na'):
                    ind_offset = offset.rsplit(',')
                    for roffset in ind_offset:
                        offset_splt = roffset.rsplit(':')
                        if(offset_splt[0]==screen_name):
                            offset_in = int(offset_splt[1])
                            break
                        else:
                            offset_in = 0
                else:
                    offset_in = 0
                print("Offset:", offset_in)
                available_seat = (section['sAvail'])
                if(total_seat-available_seat < offset_in):
                    offset_in = 0
                available_seats += (available_seat + offset_in)
                booked_seat = total_seat-(available_seat + offset_in)
                price = price + (section['price'] * booked_seat)
                print("Category Name:", category_name)
                print("Total:",total_seat)
                print("Available: ",available_seat + offset_in)
                print("Booked:",booked_seat)
                print("Price",price)
                cur_time=datetime_NY.strftime('%d/%m/%Y %I:%M %p')  
        if(show_count != 0):
            print("Shows",show_count)
            payload ={"show_date": ptm_date,"show_count":show_count,"category_name": category_name,"theatre_name":theatre_name,"price": price,"booked_seats": total_seats-available_seats,"available_seats": available_seats,"total_seats": total_seats,"theatre_code": theatre_code,"theatre_location": city,"last_modified": cur_time,"film": bm_id}
            putt = requests.put('http://flicktracks.herokuapp.com/api/porgdata/'+str(theatre_code)+'/'+ptm_date+'/'+bm_id+'/',json=payload, headers={'Content-type': 'application/json'})
            print(type(ptm_date),type(bm_id),type(theatre_code))
            print("Status Code:",putt.status_code)

film_data= requests.get('http://flicktracks.herokuapp.com/api/films/').text
film_data_json = json.loads(film_data)
locData = requests.get('http://flicktracks.herokuapp.com/api/tracks/').text
locData_json = json.loads(locData)
for film in film_data_json:
    if (film['film_status']!='stopped'):
        for loc in locData_json:
            if (loc['is_currently_tracking']!='no' or loc['is_currently_tracking']!='N'):
                if(loc['source']=='bms'):
                    new_algo_bm(film['film_name'],film['film_id'],loc['track_location'],loc['loc_real_name'],loc['theatre_code'])
                if(film['ptm_code']!='NA') and (loc['source']=='ptm'):
                    new_algo_ptm(film['ptm_code'],loc['theatre_code'],loc['track_location'], film['film_id'],loc['offset_check'])

          

from urllib import request
import requests
import json
from bs4 import BeautifulSoup
import pytz
from datetime import datetime
import re

def ptm_track(code,ptm_theatre_id,city,bm_id,offset):
    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY)
    
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
                        booked_seat = total_seat-available_seat
                        price = section['price']
                        print("Category Name:", category_name)
                        print("Total:",total_seat)
                        print("Available: ",available_seat)
                        print("Booked:",booked_seat)
                        print("Price",price)
                        cur_time=datetime_NY.strftime('%I:%M %p')
                        payload ={"show_id": show_id,"theatre_name":theatre_name,"show_time": ptm_time,"screen_name": screen_name,"show_date": ptm_date,"category_name": category_name,"price": price,"booked_seats": booked_seat,"available_seats": available_seat,"total_seats": total_seat,"theatre_code": theatre_code,"theatre_location": city,"last_modified": cur_time,"film": bm_id}
                    print("------------------------------------------")


film_data= requests.get('http://flicktracks.herokuapp.com/api/films/').text
film_data_json = json.loads(film_data)
locData = requests.get('http://flicktracks.herokuapp.com/api/tracks/').text
locData_json = json.loads(locData)
for film in film_data_json:
    if(film['film_status']!='inactive') and (film['ptm_code']!='NA'):
        for loc in locData_json:
            if(loc['is_currently_tracking']!='no' or loc['is_currently_tracking']!='N') and (loc['source']=='ptm'):
                ptm_track('bote0jbze','2661','kozhikode', film['film_id'],loc['offset'])
                
# location = 'kozhikode'
# ptm_film_id = 'nvrmir2cs'
# ptm_theatre_id = '2661'
# bm_id = 'bms_id'
# ptm_track(ptm_film_id,ptm_theatre_id,location, bm_id)


# for film in film_data_json:
#     if(film['film_status']!='inactive') and (film['ptm_code']!='NA'):
#         for loc in locData_json:
#             if(loc['is_currently_tracking']!='no' or loc['is_currently_tracking']!='N') and (loc['source']=='ptm'):
#                 ptm_track(film['ptm_code'],'2661','kozhikode', film['film_id'])
            
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import pytz

def tn_process(location,venue_code,film_id,movie_code,tkt_price):
    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY)
    tktnewUrl = "https://www.ticketnew.com/test/Online-Advance-Booking/"+movie_code+"/C/"+location+"/"
    requ = requests.get(tktnewUrl)
    html = BeautifulSoup(requ.content,"html.parser")
    movie_name = html.find("div",class_='movie-details tn-entity-details')
    query = html.find_all("a",{'data-venue':True,'data-venue':venue_code})
    for val in query:
        print(movie_name.h2.text)
        # print(val['data-venuen'])
        # print(val["data-tkts"])
        show_time = val.text
        date = val['data-date'].rsplit('-')
        show_date = date[0]+date[1]+date[2]
        print("Show Date:",show_date)
        print("Show Time:",show_time)
        show_id = val["data-event"]
        theatre_name = val["data-venuen"]
        screen_name = val["data-screenn"]
        print("Theatre Name: ", theatre_name)
        print("Screen Name:", screen_name)
        print("Theatr Location:", location)
        # print("Data: ",val["data-tkts"])
        jss =str(val["data-tkts"])
        dictt = json.loads(jss)
        for row in dictt:
            try:
                
                category_name = row["Name"]
                
                total_seat = row["Total"]
                available_seat = row["Avail"]
                booked_seat = total_seat - available_seat
                print("Class:", category_name)
                print("|----Booked Seats:",booked_seat)
                print("|----Available Seats: ",available_seat)
                print("|----Total Seats: ",total_seat)
                price = row['Rate']
                if not price == 0.0:
                    print("|----Price: ",row['Rate'])
                else:
                    price = tkt_price
                    print("|----Price: ",tkt_price)
                cur_time=datetime_NY.strftime('%I:%M %p')
                print("Last Modified:", cur_time)
                payload ={"show_id": show_id,"theatre_name":theatre_name,"show_time": show_time,"screen_name": screen_name,"show_date": show_date,"category_name": category_name,"price": price,"booked_seats": booked_seat,"available_seats": available_seat,"total_seats": total_seat,"theatre_code": venue_code,"theatre_location": location,"last_modified": cur_time,"film": film_id}
                
            except AttributeError:
                print("Not found")
        print("-------------------------------------")



film_data= requests.get('http://flicktracks.herokuapp.com/api/films/').text
film_data_json = json.loads(film_data)
locData = requests.get('http://flicktracks.herokuapp.com/api/tracks/').text
locData_json = json.loads(locData)
for film in film_data_json:
    if(film['film_status']!='inactive') and (film['tn_code']!='NA'):
        for loc in locData_json:
            if(loc['is_currently_tracking']!='no' or loc['is_currently_tracking']!='N') and (loc['source']=='tn'):
                tn_process(loc['track_location'],loc['theatre_code'],film['film_id'],film['tn_code'],'120.0')


                
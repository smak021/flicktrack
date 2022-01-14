from datetime import datetime,timedelta
import json
from operator import add
import pytz
from requests.models import Response
import schedule
import time
import requests

#Read all
#page = requests.get('http://127.0.0.1:8000/hello')
#print(page.json())

#add one row
#query1 = {'film_name': 'huh', 'film_id':'ere', 'theatre_id': 'eeew', 'show_id': 'ewf','available_seat': 101, 'total_seat': 130, 'booked_seat': 30, 'Show_time': '10:10:11', 'show_date': '2021-12-04', 'last_modified': '2022-01-12' }
#query1_json=json.dumps(query1)
#r= requests.post('http://127.0.0.1:8000/hello', data = query1_json, headers={'Content-type': 'application/json'})
#url = r.text
#print(url)

#delete
#page = requests.delete('http://127.0.0.1:8000/hi/2')

#update
#query1 = {"film_name": "huh", "film_id": "khjhlere", "theatre_id": "eeew", "show_id": "ewf", "available_seat": 101, "total_seat": 130, "booked_seat": 40, "Show_time": "10:10:11", "show_date": "2021-12-04", "last_modified": "2022-01-12"}
#query1_json=json.dumps(query1)
#r= requests.put('http://127.0.0.1:8000/hi/4/', json= query1, headers={'Content-type': 'application/json'})


'''time="10:20 PM"
tz_NY = pytz.timezone('Asia/Kolkata')   
datetime_NY = datetime.now(tz_NY)
tmwopm=time.rsplit(' ',1)[-2]
tmhr=time.rsplit(':',1)[-2]
tmmin=tmwopm.rsplit(':',1)[-1]
tmampm=time.rsplit(' ',1)[-1]
cur_time=datetime_NY.strftime('%I:%M %p')
print(time)
print(tmhr)
print(tmmin)
print(tmampm)
print(cur_time.rsplit(':',1)[-2])'''

'''def timesplit(time):
    tmwopm=time.rsplit(' ',1)[-2]
    tmhr=time.rsplit(':',1)[-2]
    tmmin=tmwopm.rsplit(':',1)[-1]
    tmampm=time.rsplit(' ',1)[-1]
    return [tmhr,tmmin,tmampm]

tz_NY = pytz.timezone('Asia/Kolkata')   
datetime_NY = datetime.now(tz_NY)

stim="02:56 PM"
stim2="02:55 AM"
d1 =stim
cur_time=datetime.strptime(d1,'%I:%M %p')
add_time =cur_time+timedelta(minutes=10)
nw_time=add_time.strftime('%I:%M %p')
print(d1)
if stim < stim2:
    print("true")
else:
    print("false")
print(cur_time)
print(add_time)
print(nw_time)'''
'''timee=timesplit(cur_time)
stim="02:56 PM"
tim=timesplit(stim)
if cur_time==stim:
    print("stop tracking")
else:
    print("Track")
'''
fm_loc="KOZH"
uu= requests.get('http://127.0.0.1:8000/getlocdata/').text
json_data=json.loads(uu)
for fmlo in json_data:
    print(fmlo['film_location'])
    if fmlo['film_location'] == fm_loc:
        loc_slug=fmlo['venue_id']
        
    else:
        loc_slug="Not available"

print(loc_slug)


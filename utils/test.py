import requests
import json
from bs4 import BeautifulSoup
from difflib import SequenceMatcher


film_data= requests.get('http://flicktracks.herokuapp.com/api/films/').text
film_data_json = json.loads(film_data)
for film in film_data_json:
    bms_id = film['full_name']
    test = bms_id.rsplit('(')
    print(test[0])


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

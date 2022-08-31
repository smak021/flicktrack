from telnetlib import TN3270E
import requests
import json
from bs4 import BeautifulSoup
from difflib import SequenceMatcher




film_data= requests.get('http://flicktracks.herokuapp.com/api/films/').text
film_data_json = json.loads(film_data)
locData = requests.get('http://flicktracks.herokuapp.com/api/tracks/').text
locData_json = json.loads(locData)
for film in film_data_json:
    if(film['film_status']!='inactive' or film['film_status']!='stopped'):
        for loc in locData_json:
            if(loc['is_currently_tracking']!='no' or loc['is_currently_tracking']!='N') :
                bms()
                if(film['ptm_code']!='NA') and (loc['source']=='ptm'):
                    paytm()
                if(film['tn_code']!='NA') and (loc['source']=='tn'):
                    tn()
                
                


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

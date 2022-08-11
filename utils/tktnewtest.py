import json
from turtle import ht
from bs4 import BeautifulSoup
import requests

# Ticket New

tktnewUrl = "https://www.ticketnew.com/Nna-Thaan-Case-Kodu--Movie-Tickets-Online-Show-Timings/Online-Advance-Booking/25382/C/Calicut"

requ = requests.get(tktnewUrl)
html = BeautifulSoup(requ.content,"html.parser")
query = html.find_all("div",class_="tn-timing-details")
for val in query:
    for val2 in val.ul:
        # print(val2.li.a["data-venuen"])
        # print(val2.li.a["data-tkts"])
        try:
            print(val2.a["data-venuen"])
            print(val2.a["data-tkts"])
        except AttributeError:
            print("Not found")
    # print(val.ul.li.a)



# venue_url=requests.get("https://in.bookmyshow.com/serv/getData?cmd=VENUESHOWCASE&venueCode=ATTR").text
# vjson = json.loads(venue_url)
# print(vjson['data']['venueName'])


# url = requests.get("https://in.bookmyshow.com/kozhikode/movies/kaduva/ET00330368")
# html = BeautifulSoup(url.content,"html.parser")
# query = html.find("section",id="component-4")
# actors={}
# crew={}
# castscrap = query.a['class'][0]
# print(query.a['class'][0])
# query2 = html.find_all("a",class_=castscrap)
# count =0
# for val in query2:
#     if val.h5.parent.parent.parent.parent.parent['id'] == 'component-4':
#         actors["Actor "+str(count)]  = val.h5.string
#     else:
#         crew["Crew "+str(count)]  = val.h5.string
#     count +=1


# castncrew = {'actors':actors,'crews':crew}
# jsonval = json.dumps(castncrew)
# print(jsonval)
# # for values in query:
# #     print(query.h5.string)
# #     print(values)


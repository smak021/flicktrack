import json
import string
from turtle import ht
from bs4 import BeautifulSoup
import requests
import ast

# Ticket New
location='Mukkam'
venue_code = '15123'
# movie_text ='Nna-Thaan-Case-Kodu--Movie-Tickets-Online-Show-Timings'
movie_code= '25382'
t_price ='120.0'
tktnewUrl = "https://www.ticketnew.com/test/Online-Advance-Booking/"+movie_code+"/C/"+location+"/"
requ = requests.get(tktnewUrl)
html = BeautifulSoup(requ.content,"html.parser")
movie_name = html.find("div",class_='movie-details tn-entity-details')
query = html.find_all("a",{'data-venue':True,'data-venue':venue_code})
for val in query:
    print(movie_name.h2.string)
    # print(val['data-venuen'])
    # print(val["data-tkts"])
    print("Theatre Name: ",val["data-venuen"])
    print("Venue: ",val["data-venue"])
    # print("Data: ",val["data-tkts"])
    jss =str(val["data-tkts"])
    dictt = json.loads(jss)
    for row in dictt:
        try:
            print("Class:", row["Name"])
            print("|----Available Seats: ",row["Avail"])
            print("|----Total Seats: ",row["Total"])
            price = row['Rate']
            if not price == 0.0:
                print("|----Price: ",row['Rate'])
            else:
                print("|----Price: ",t_price)
        except AttributeError:
            print("Not found")
    print("-------------------------------------")

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


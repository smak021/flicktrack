import json
from turtle import ht
from bs4 import BeautifulSoup
import requests

url = "https://www.ticketnew.com/online-advance-booking/Movies/C"

requ = requests.get(url+"/Calicut")
html = BeautifulSoup(requ.content,"html.parser")
query = html.find("div",id="now_showing")
for val in query:
    for val2 in val:
        print(val2.h4.text)
        print(val2.a["href"])
    #     # print(val.div.a["href"])

#    print(val.a)

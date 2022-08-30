from urllib import request
import requests
import json
from bs4 import BeautifulSoup
import pytz
import re

city = 'kozhikode'
website = 'https://paytm.com/movies/'+city
page = requests.get(website,cookies={'movies_city': city})
soup = BeautifulSoup(page.content, "html.parser")
ssid= soup.find('script',id='__NEXT_DATA__')
data = ssid.text
jsonData =  json.loads(data)
for data in jsonData['props']['pageProps']['initialState']['movies']['currentlyRunningMovies'][city]['groupedMovies']:
    print(data['label'])
    print(data['languageFormatGroups'][0]['fmtGrpId'])
    code = data['languageFormatGroups'][0]['fmtGrpId']
    url = "https://apiproxy.paytm.com/v3/movies/search/movie?meta=1&reqData=1&city="+city+"&movieCode="+code+"&version=3&site_id=1&channel=HTML5&child_site_id=1" 
    data = requests.get(url).text
    json_data = json.loads(data)
    # print("theatre:",json_data['meta']['cinemas'][0]['name'])
    # print(json_data['pageData']['sessions'])
    for row in json_data['pageData']['sessions']:
        for show in json_data['pageData']['sessions'][row]:
            try:
                pid = show['pid']
                my_item = next((item for item in json_data['meta']['cinemas'] if item['pid'] == pid), None)
                print("Theatre:",my_item['name'])
                print("Show_id:", show['sid'])
                print("theatre_id:", show['pid'])
                print("Screen: ",show['audi'])
                for section in show['areas']:
                    print("Category Name:", section['label'])
                    print("Total:",section['sTotal'])
                    print("Available: ",section['sAvail'])
                    print(section['price'])
              
            except KeyError:
                print("not found")
            print("------------------------------------------")
postman = "https://apiproxy.paytm.com/v3/movies/search/movie?meta=1&reqData=1&city=kottakkal&movieCode=umt%7Epab0oz&version=3&site_id=1&channel=HTML5&child_site_id=1"
# print(jsonData['props']['pageProps']['initialState']['movies']['currentlyRunningMovies']['kottakkal']['groupedMovies'][0]['languageFormatGroups'][0]['fmtGrpId'])
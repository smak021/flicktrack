import requests
import json
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

city = 'kochi'
website = 'https://paytm.com/movies/'+city
page = requests.get(website,cookies={'movies_city': city})
soup = BeautifulSoup(page.content, "html.parser")
ssid= soup.find('script',id='__NEXT_DATA__')
data = ssid.text
jsonData =  json.loads(data)
for data in jsonData['props']['pageProps']['initialState']['movies']['currentlyRunningMovies'][city]['groupedMovies']:
    print("Film Name:",data['label'])
    film_name = data['label']
    ptm_code = data['languageFormatGroups'][0]['fmtGrpId']
    print("Paytm Code:",data['languageFormatGroups'][0]['fmtGrpId'])
    code = data['languageFormatGroups'][0]['fmtGrpId']
    film_data= requests.get('http://flicktracks.herokuapp.com/api/films/').text
    film_data_json = json.loads(film_data)
    for film in film_data_json:
        bms_id = film['film_id']
        bms_name = film['full_name']
        test = bms_name.rsplit('(')
        bms_name = test[0]
        print("BMS NAme:",bms_name)
        print("Paytm Film Name:",data['label'])
        # print("Checking", movie_id, film['full_name'])
        check_match = SequenceMatcher(None,film_name.lower(),bms_name.lower()).ratio()
        # print(check_match)
        if check_match>0.8:
            print("Passed")
            print(bms_id)
            payload = {"ptm_code":ptm_code}
            putData =requests.put('http://flicktracks.herokuapp.com/api/upfilm/'+bms_id, json=payload, headers={'Content-type': 'application/json'})
            print(putData.status_code)
            break
        print("-----------------")
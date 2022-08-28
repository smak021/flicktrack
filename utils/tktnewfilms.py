import json
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import requests

url = "https://www.ticketnew.com/online-advance-booking/Movies/C"

requ = requests.get(url+"/Kochi")
html = BeautifulSoup(requ.content,"html.parser")
query = html.find("div",id="now_showing")
for val in query:
    for val2 in val:
        movie_id = val2.a.img['alt']
        print("Movie ID:",movie_id)
        # Check id with film table.
        print("Movie Name:",val2.h4.text)

        m_link = val2.a["href"]
        split = m_link.rsplit('/',5)
        m_code = split[-3]
        m_link_cut = split[-5]
        print("Movie Link Code:",m_link_cut)
        print("Movie Code:",m_code)
        film_data= requests.get('http://flicktracks.herokuapp.com/api/films/').text
        film_data_json = json.loads(film_data)
        for film in film_data_json:
            bms_id = film['film_id']
            print("Checking", movie_id, film['full_name'])
            check_match = SequenceMatcher(None,movie_id.lower(),film['full_name'].lower()).ratio()
            # print(check_match)
            if check_match>0.8:
                print("Passed")
                print(bms_id)
                payload = {"tn_code":m_code}
                putData =requests.put('http://flicktracks.herokuapp.com/api/putfilm/'+bms_id+'/', json=payload, headers={'Content-type': 'application/json'})
                print(putData.status_code)
        # print("Movie_Link:",val2.a["href"])

        print("---------------------------")
    #     # print(val.div.a["href"])

#    print(val.a)

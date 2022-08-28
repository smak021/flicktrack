import requests
import json
from difflib import SequenceMatcher
from bs4 import BeautifulSoup

# BeEmEs Function
def bms_calc():
    json_data=['KOZH','TRIV','KOCH']
    # uu= requests.get('http://flicktracks.herokuapp.com/api/tracks/').text
    # json_data=json.loads(uu)
    for fmlo in json_data:
        # loc = fmlo['track_location']
        loc = fmlo
        payload='{"bmsId":"1.760661160.1633786977283","regionCode":"'+loc+'","isSuperstar":"N"}'
        print(payload)
        requests.adapters.DEFAULT_RETRIES = 5
        url = requests.post('https://in.bookmyshow.com/pwa/api/uapi/movies',data=payload ,headers={'content-type':'application/json'}).text 
        url_json = json.loads(url)
        substring = 'bookmyshow.com'
        for i in url_json["nowShowing"]["arrEvents"]:
            film_name = str(i["ChildEvents"][0]['EventURL'])
            film_real_name=str(i["ChildEvents"][0]['EventName'])
            print(film_name)
            film_id = str(i["ChildEvents"][0]['EventCode'])
            release_date = str(i["ChildEvents"][0]['EventDate'])
            image_url = str(i["ChildEvents"][0]['EventImageCode'])
            film_length=str(i["ChildEvents"][0]['Duration'])
            film_genre=str(i["ChildEvents"][0]['EventGenre'])
            film_censor=str(i["ChildEvents"][0]['EventCensor'])
            film_loc = str(i["ChildEvents"][0]['RegCode'])
            # Scrapping film story from site
            storyurl = requests.get("https://in.bookmyshow.com/"+loc+"/movies/"+film_name+"/"+film_id)
            html = BeautifulSoup(storyurl.content,"html.parser")
            query = html.find("section",id="component-1")
            film_story = query.span.span.string
            #end of scrap
            #scrap cast n crew
            actors=[]
            crew=[]
            ccquery = html.find("section",id="component-4")
            try:
                classname =  ccquery.a['class'][0]
                readquery = html.find_all("a",class_=classname)
            except AttributeError:
                readquery = None
            # acount =0
            # ccount =0
            if readquery != None:
                for val in readquery:
                    if val.h5.parent.parent.parent.parent.parent['id'] == 'component-4':
                        if val.h5.string != None:
                            actors.append(val.h5.string)
                        else:
                            actors.append('NA')
                    else:
                        if val.h5.string != None:
                            crew.append(val.h5.string)
                        else:
                            actors.append('NA')
            else:
                actors=["NA","NA"]
                crew = ["NA"]
            actors.append("NA")
            crew.append("NA")
            castncrew = {'actors':actors,'crews':crew}
            jsoncastncrew = json.dumps(castncrew)
            # end cast n crew scrap
            if film_story!= None and substring in film_story:
                film_story='Not Available'
            print(film_loc)
            payload1={"film_id":film_id,"film_name": film_name, "cover_url":image_url, "release_date": release_date,"film_story":film_story,"film_genre":film_genre,"film_censor":film_censor,"film_duration":film_length,"full_name":film_real_name,"cast_n_crew":jsoncastncrew}
            payload2 = {"film_id":film_id,"is_tracking":True}
            payload1_json = json.dumps(payload1)
            url1=requests.put('http://flicktracks.herokuapp.com/api/putfilm/'+film_id+'/', json=payload1, headers={'Content-type': 'application/json'})
            url2 = requests.put('http://flicktracks.herokuapp.com/api/status/',json=payload2,headers={'Content-type': 'application/json'})
            #print(url1.text)

# TktNw Function

def tn_calc():    
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
                # print("Checking", movie_id, film['full_name'])
                check_match = SequenceMatcher(None,movie_id.lower(),film['full_name'].lower()).ratio()
                # print(check_match)
                if check_match>0.8:
                    print("Passed")
                    print(bms_id)
                    payload = {"tn_code":m_code}
                    putData =requests.put('http://flicktracks.herokuapp.com/api/upfilm/'+bms_id, json=payload, headers={'Content-type': 'application/json'})
                    print(putData.status_code)
            # print("Movie_Link:",val2.a["href"])
            print("---------------------------")

bms_calc()
tn_calc()


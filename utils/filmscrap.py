import requests
import json
from difflib import SequenceMatcher
from bs4 import BeautifulSoup
import cloudscraper

# BeEmEs Function
def bms_calc():
    json_data=['KOCH','KOZH','TRIV']
    # uu= requests.get('http://flicktracks.herokuapp.com/api/tracks/').text
    # json_data=json.loads(uu)
    for fmlo in json_data:
        # loc = fmlo['track_location']
        loc = fmlo
        substring = 'email protected'
        payload='{"bmsId":"1.2572928712.1661954374374","regionCode":"'+loc+'","isSuperstar":"N"}'
        print(payload)
        requests.adapters.DEFAULT_RETRIES = 5
        try:
            scrapper = cloudscraper.create_scraper()
            url = scrapper.post('https://in.bookmyshow.com/pwa/api/uapi/movies',data=payload,headers={'content-type':'application/json'}) 
            # print(url.text)
            url_json = json.loads(url.text)
        except:
            print("Error reading url")
            url_json = False
        else:
            for i in url_json["nowShowing"]["arrEvents"]:
                for film in i["ChildEvents"]:
                    film_name = str(film['EventURL'])
                    film_real_name=str(film['EventName'])
                    print(film_name)
                    film_id = str(film['EventCode'])
                    print(film_id)
                    release_date = str(film['EventDate'])
                    image_url = str(film['EventImageCode'])
                    film_length=str(film['Duration'])
                    film_genre=str(film['EventGenre'])
                    language = str(film['EventLanguage'])
                    film_censor=str(film['EventCensor'])
                    film_loc = str(film['RegCode'])
                    # Scrapping film story from site
                    try:
                        print(loc,film_name,film_id)
                        scrapper = cloudscraper.create_scraper()
                        storyurl = scrapper.get("https://in.bookmyshow.com/"+loc+"/movies/"+film_name+"/"+film_id)
                        html = BeautifulSoup(storyurl.content,"html.parser")
                        query = html.find("section",id="component-1")
                        film_story = query.span.span.text
                        # print(film_story)
                        #end of scrap
                        #scrap cast n crew
                        actors=[]
                        crew=[]
                        ccquery = html.find("section",id="component-4")
                        classname =  ccquery.a['class'][0]
                        readquery = html.find_all("a",class_=classname)
                    except AttributeError:
                        print("Attribute Error: Error reading story / cast")
                        actors=["NA","NA"]
                        crew = ["NA"]
                        film_story='Not Available'
                    except:
                        print('Error')
                        
                    # acount =0
                    # ccount =0
                    else:
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
                    actors.append("NA")
                    crew.append("NA")
                    castncrew = {'actors':actors,'crews':crew}
                    # jsoncastncrew = json.dumps(castncrew)
                    # end cast n crew scrap
                    if (film_story!= None and substring in film_story):
                        film_story='Not Available'
                    print(film_loc)
                    payload1={"film_id":film_id,"film_name": film_name, "cover_url":image_url,"language":language, "release_date": release_date,"film_story":film_story,"film_genre":film_genre,"film_censor":film_censor,"film_duration":film_length,"full_name":film_real_name,"cast_n_crew":castncrew}
                    url1=requests.put('http://flicktracks.herokuapp.com/api/putfilm/'+film_id+'/', json=payload1, headers={'Content-type': 'application/json'})
                    print(url1.status_code)


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

def ptm_calc():     
    locations = ['kochi','kozhikode']
    for city in locations:
        print(city)
        website = 'https://paytm.com/movies/'+city
        page = requests.get(website,cookies={'movies_city': city})
        soup = BeautifulSoup(page.content, "html.parser")
        ssid= soup.find('script',id='__NEXT_DATA__')
        data = ssid.text
        jsonData =  json.loads(data)
        for data in jsonData['props']['pageProps']['initialState']['movies']['currentlyRunningMovies'][city]['groupedMovies']:
            print("Film Name:",data['label'])
            film_name = data['label'].rsplit('(')[0]
            for language in data['languageFormatGroups']:
                film_language = language['lang']
                ptm_code = language['fmtGrpId']
                print("Paytm Code:",language['fmtGrpId'])
                film_data= requests.get('http://flicktracks.herokuapp.com/api/films/').text
                film_data_json = json.loads(film_data)
                for film in film_data_json:
                    bms_id = film['film_id']
                    bms_name = film['full_name']
                    bms_lang = film['language']
                    test = bms_name.rsplit('(')
                    bms_name = test[0]
                    print("BMS NAme:",bms_name)
                    print("Paytm Film Name:",data['label'])
                    check_match = SequenceMatcher(None,film_name.lower(),bms_name.lower()).ratio()
                    language_match = SequenceMatcher(None,bms_lang.lower(),film_language.lower()).ratio()
                    # print(check_match)
                    if check_match>0.8 and (language_match>0.8):
                        print("Passed")
                        print(bms_id)
                        payload = {"ptm_code":ptm_code}
                        putData =requests.put('http://flicktracks.herokuapp.com/api/upfilm/'+bms_id, json=payload, headers={'Content-type': 'application/json'})
                        print(putData.status_code)
                        break
                    print("-----------------")

bms_calc()
# tn_calc()
ptm_calc()

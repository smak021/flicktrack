import requests
import json
import pytz

uu= requests.get('http://127.0.0.1:8000/api/tracks/').text
json_data=json.loads(uu)
for fmlo in json_data:
    loc = fmlo['track_location']
    payload='{"bmsId":"1.760661160.1633786977283","regionCode":"'+loc+'","isSuperstar":"N"}'
    print(payload)
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
        film_story=str(i["ChildEvents"][0]['EventSynopsis'])
        film_censor=str(i["ChildEvents"][0]['EventCensor'])
        film_loc = str(i["ChildEvents"][0]['RegCode'])
        if film_story!= None and substring in film_story:
            film_story='Not Available'
        print(film_loc)
        payload1={"film_id":film_id,"film_name": film_name, "cover_url":image_url, "release_date": release_date,"film_story":film_story,"film_genre":film_genre,"film_censor":film_censor,"film_duration":film_length}
        payload1_json = json.dumps(payload1)
        url1=requests.put('http://127.0.0.1:8000/api/putfilm/'+film_id+'/', json=payload1, headers={'Content-type': 'application/json'})
        #print(url1.text)


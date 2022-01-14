import requests
import json
import pytz

uu= requests.get('http://127.0.0.1:8000/getlocdata/').text
json_data=json.loads(uu)
for fmlo in json_data:
    payload='{"bmsId":"1.760661160.1633786977283","regionCode":"'+fmlo['film_location']+'","isSuperstar":"N"}'
    url = requests.post('https://in.bookmyshow.com/pwa/api/uapi/movies',data=payload ,headers={'content-type':'application/json'}).text
    url_json = json.loads(url)
    for i in url_json["nowShowing"]["arrEvents"]:
        film_name = str(i["ChildEvents"][0]['EventURL'])
        print(film_name)
        film_id = str(i["ChildEvents"][0]['EventCode'])
        release_date = str(i["ChildEvents"][0]['EventDate'])
        film_loc = str(i["ChildEvents"][0]['RegCode'])
        print(film_loc)
        payload1={"film_name": film_name, "film_id": film_id, "release_date": release_date, "film_loc":film_loc}
        payload1_json = json.dumps(payload1)
        url1=requests.put('http://127.0.0.1:8000/getfilmdata/'+film_id+'/'+film_loc+'/', json=payload1, headers={'Content-type': 'application/json'})
        print(url1.text)


import requests
import json
from bs4 import BeautifulSoup

venue_url=requests.get('https://in.bookmyshow.com/serv/getData?cmd=VENUESHOWCASE&venueCode=CNOT').text
vjson = json.loads(venue_url)
theatre_name = vjson['data']['venueName']

print(theatre_name)

import requests
import json
from bs4 import BeautifulSoup
from difflib import SequenceMatcher


#BMS - Ticket New Linking by comparing
bms_title = 'yatraa'

tktnew_title = "Yathra"

check_match = SequenceMatcher(None,tktnew_title.lower(),bms_title.lower()).ratio()
print(check_match)

if check_match>0.8:
    print("Matches")
else:
    print("No Match")

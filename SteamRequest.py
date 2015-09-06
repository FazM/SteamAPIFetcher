__author__ = 'Faz'
import sys
#sys.path.append('C:\\Python34\\Lib\\site-packages\\steamapi-0.1-py3.4.egg')
"""
All interfaces and method are self-documented through the ISteamWebAPIUtil/GetSupportedAPIList call.
https://steamdb.info/

http://forums.steampowered.com/forums/showthread.php?t=2905013

FORMAT

http://api.steampowered.com/<interface>/<method>/<method_version>/.?key=<api key>&format=<format>

Steam Web APIs available
ISteamNews: Steam provides methods to fetch news feeds for each Steam game.
ISteamUserStats: Steam provides methods to fetch global stat information by game.
ISteamUser: Steam provides API calls to provide information about Steam users.
ITFItems_440: Team Fortress 2 provides API calls to use when accessing player item data.
"""


import requests
import key
import json
from bs4 import BeautifulSoup
import pprint as pp


API_KEY = key.API_PRIVATE_KEY

t = requests.get('http://api.steampowered.com/ISteamWebAPIUtil/GetSupportedAPIList/v0001/?format=json')
r = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={KEY}&steamids=STEAM_ID'.format(KEY=API_KEY))
teamfortress2  = requests.get('http://api.steampowered.com/ISteamNews/GetNewsForApp/v0001/?format=xml&appid=440&count=3')

data = json.loads(r.text)
data2 = json.loads(t.text)
xmltext = BeautifulSoup(teamfortress2.text)

print(pp.pprint(data2['apilist']['interfaces']))



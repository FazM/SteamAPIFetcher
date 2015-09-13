__author__ = 'Faz'
import key
import requests
import json


"""
API GET CALLS:
http://api.steampowered.com/<interface name>/<method name>/v<version>/?key=<api key>&format=<format>.

<format>:
json (DEFAULT) - The output will be returned in the JSON format
xml - Output is returned as an XML document
vdf - Output is returned as a VDF file.

My Profile:
http://steamcommunity.com/id/thisisfaz/
my steamid : 76561198066178099
"""

# Global Variables
BASE_URL = 'https://api.steampowered.com/'
API_KEY = key.API_PRIVATE_KEY
INTERFACE_DICT = {'user_stats' : 'ISteamUser',
                  'app_stats' : 'ISteamUserStats',
                  'news_stats' : 'ISteamNews',}


# dynamically generate URL for API GET calls
def api_url(interface, method, private_key=API_KEY, version = 'v1',  **kwargs):

    URL = '{DOMAIN}{INTERFACE}/{METHOD}/{VERSION}/?key={PRIVATE_KEY}'.format(DOMAIN=BASE_URL,
                                                                             INTERFACE=interface,
                                                                             METHOD=method,
                                                                             VERSION=version,
                                                                             PRIVATE_KEY=private_key)

    for name, params in kwargs.items():
        URL = URL + '&{0}={1}'.format(name, params)
    return URL

# input URL path
# and output JSON object
def url_to_json(URL):

    url_file = requests.get(URL)
    json_Obj = json.loads(url_file.text)
    return json_Obj


# basic app class
class App:

    def __init__ (self, app_id,):
        self.app_id = app_id

# game class extends app
class Game(App):

    def __init__ (self, app_id, description, name, tstamp):
        super().__init__(app_id) #App.__init__(self, id)
        self.description = description
        self.name = name
        self.tstamp = tstamp

    def get_game_global_stats(self):
        pass

    def get_game_price_stats(self):
        data = api_url(interface='ISteamEconomy', method='GetAssetPrices', version='v1', appid=self.app_id)
        return data

    def get_game_news_stats(self):
        pass


json = url_to_json(api_url(interface=INTERFACE_DICT['news_stats'], method = 'GetNewsForApp', format = 'json', appid='440', count=3))
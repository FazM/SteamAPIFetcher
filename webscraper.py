__author__ = 'Faz'
from bs4 import BeautifulSoup
import requests
import pprint
import pickle as cp


# global variables
game_apps = {}
apps_page = 'https://steamdb.info/apps/'

# initialise first page
html_Apps_page1 = requests.get(apps_page)
bs_Apps_page1 = BeautifulSoup(html_Apps_page1.text)

#
def find_no_of_pages(bs_Apps_page):

    soup_ul_app = bs_Apps_page.find("ul", class_="pagination")
    no_of_pages = int(soup_ul_app.find_all('li')[-1].find('a').get_text())
    return no_of_pages

#
def web_page_generator(no_of_pages):

    pages = [apps_page]
    for page_no in range (2, no_of_pages):
        pages.append(apps_page + 'page{page_n}/'.format(page_n=str(page_no)))

    return pages


no_of_pages = find_no_of_pages(bs_Apps_page1)
page_urls = web_page_generator(no_of_pages)

index = 0

for page_url in page_urls:

    html_Apps_page = requests.get(page_url)
    bs_Apps_page = BeautifulSoup(html_Apps_page.text)
    ts_Elements = bs_Apps_page.find_all("tr", class_="app")

    for app in ts_Elements:

        app_id, \
        app_description, \
        app_name, \
        app_tstamp = [td_content.get_text() for td_content in app.find_all("td")]

        if app_description == 'Game' and \
                app.find('a', attrs={'aria-label': 'This app is in store'}):

            game_apps[app_id] = {}
            game_apps[app_id]['app_name'] = app_name.replace('\n' , '')
            game_apps[app_id]['app_tstamp'] = app_tstamp

    index +=1
    print('page {page_no} completed'.format(page_no=index))
    print(len(game_apps))

# lets dump our {} list in gameapps.pickle
with open('gameapps.pickle', 'wb') as f:
    cp.dump(game_apps, f)

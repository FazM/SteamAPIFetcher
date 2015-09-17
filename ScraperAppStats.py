__author__ = 'Faz'

"""
insert decription here
"""


from bs4 import BeautifulSoup
import requests
import pickle as cp

# global variables
game_apps = {}
apps_page = 'https://steamdb.info/apps/'
pickle_path = 'gameapps.pickle'

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

    for page_no in range (2, no_of_pages):
        yield (apps_page + 'page{page_n}/'.format(page_n=str(page_no)))

#
def generate_game_stats_from_url(url_list):
    index = 0
    for page_url in url_list:
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

    return game_apps

#
def dump_to_pickle_file(object):
    # lets dump our {} list in gameapps.pickle
    with open(pickle_path, 'wb') as f:
        cp.dump(object, f)

no_of_pages = find_no_of_pages(bs_Apps_page1)
page_urls = web_page_generator(no_of_pages)
game_apps_dict = generate_game_stats_from_url(url_list = page_urls)
dump_to_pickle_file(game_apps_dict)


# LOOK AT SUPER-PYTHON
# LOOK AT GRABBING GAME TYPE FROM CHILD PAGES AND APP IDS I.E ACTION, PLATFORMER ECT

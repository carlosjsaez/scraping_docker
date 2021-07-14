import urllib.request
from bs4 import BeautifulSoup
import mysql.connector
import logging
print('test')
logging.debug('please')
print('pleaseprint')
# logging.basicConfig(level=logging.DEBUG)


url_ini = 'https://www.urparts.com/index.cfm/page/catalogue'
hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }

req = urllib.request.Request(url_ini, headers=hdr)
response = urllib.request.urlopen(req)

soup = BeautifulSoup(response.read(), 'lxml')

res = []

tags = [tag.get_text().strip() for tag in soup.select('div[class="c_container allmakes"]')[0].findAll('a')]

for tag in tags[0:1]:
    logging.debug(tag)
    print(tag)
    # tag = tags[0]
    url = f'{url_ini}/{tag}'
    url = url.replace(' ', '%20')
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response.read(), 'lxml')
    cats = [cat.get_text().strip() for cat in soup.select('div[class="c_container allmakes allcategories"]')[0].findAll('a')]

    for cat in cats[0:1]:
        logging.debug(cat)
        print(cat)
        # cat = cats[0]
        url = f'{url_ini}/{tag}/{cat}'
        url = url.replace(' ', '%20')
        req = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(req)
        soup = BeautifulSoup(response.read(), 'lxml')
        models = [model.get_text().strip() for model in soup.select('div[class="c_container allmodels"]')[0].findAll('a')]

        for model in models[0:1]:
            logging.debug(model)
            print(cat)
            # model = models[0]
            url = f'{url_ini}/{tag}/{cat}/{model}'
            url = url.replace(' ', '%20')
            req = urllib.request.Request(url, headers=hdr)
            response = urllib.request.urlopen(req)
            soup = BeautifulSoup(response.read(), 'lxml')
            parts = [part.get_text().strip().split(' - ') for part in soup.select('div[class="c_container allparts"]')[0].findAll('a')]
            res.extend([(tag, cat, model, part[0], part[1]) for part in parts])

# import pandas as pd
# import numpy as np
# #
# df =  pd.DataFrame(index = pd.MultiIndex.from_product([[tag],[cat], [model], parts])).reset_index()
# splitting = lambda x: x.split(' - ')
# columns = ['manufactrer', 'category', 'model', 'part', 'part_category']
#
# df.loc[:,'part'] = None
# df.loc[:,'part_category'] = None
# df.loc[:,['part', 'part_category']] = df.level_3.apply(splitting)

config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'urparts_scraper'
    }
connection = mysql.connector.connect(**config)
logging.debug(connection)

db_cursor = connection.cursor()

sql_statement = "INSERT INTO urparts_scraper.parts (manufacturer, category, model, part, part_category) values(%s, %s, %s, %s, %s)"
db_cursor.executemany(sql_statement,list(res))
connection.commit()
#
# if __name__ == '__main__':
#     scrape.run(host='0.0.0.0')
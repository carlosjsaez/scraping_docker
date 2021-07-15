import urllib.request
from bs4 import BeautifulSoup
import mysql.connector
import logging
print('test')
logging.debug('please')
print('pleaseprint')
logging.basicConfig(level=logging.DEBUG)

config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'urparts_scraper'
    }

connection = mysql.connector.connect(**config)
logging.debug(connection)

url_ini = 'https://www.urparts.com/index.cfm/page/catalogue'
hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }

req = urllib.request.Request(url_ini, headers=hdr)
response = urllib.request.urlopen(req)

soup = BeautifulSoup(response.read(), 'lxml')

tags = [tag.get_text().strip() for tag in soup.select('div[class="c_container allmakes"]')[0].findAll('a')]

for tag in tags[5:7]:
    logging.debug(tag)
    print(tag)
    res = []
    # tag = tags[0]
    url = f'{url_ini}/{tag}'
    url = url.replace(' ', '%20')
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response.read(), 'lxml')
    cats = [cat.get_text().strip() for cat in soup.select('div[class="c_container allmakes allcategories"]')[0].findAll('a')]

    for cat in cats[0:2]:
        logging.debug(cat)
        print(cat)
        # cat = cats[0]
        url = f'{url_ini}/{tag}/{cat}'
        url = url.replace(' ', '%20')
        req = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(req)
        soup = BeautifulSoup(response.read(), 'lxml')
        models = [model.get_text().strip() for model in soup.select('div[class="c_container allmodels"]')[0].findAll('a')]

        for model in models[0:2]:
            logging.debug(model)
            print(model)
            # model = models[0]
            url = f'{url_ini}/{tag}/{cat}/{model}'
            url = url.replace(' ', '%20')
            req = urllib.request.Request(url, headers=hdr)
            response = urllib.request.urlopen(req)
            soup = BeautifulSoup(response.read(), 'lxml')
            try:
                parts = [part.get_text().strip().split(' - ') for part in soup.select('div[class="c_container allparts"]')[0].findAll('a')]
                res.extend([(tag, cat, model, part[0], part[1]) for part in parts])
            except IndexError:
                print("No data found")

    db_cursor = connection.cursor()

    sql_statement = "INSERT INTO urparts_scraper.parts (manufacturer, category, model, part, part_category) values(%s, %s, %s, %s, %s)"
    db_cursor.executemany(sql_statement,list(res))
    connection.commit()
    #
# if __name__ == '__main__':
#     scrape.run(host='0.0.0.0')
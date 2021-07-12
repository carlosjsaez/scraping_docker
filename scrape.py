import urllib
from bs4 import BeautifulSoup


url_ini = 'https://www.urparts.com/index.cfm/page/catalogue'
hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }

req = urllib.request.Request(url_ini, headers=hdr)
response = urllib.request.urlopen(req)
# response.read()

soup = BeautifulSoup(response.read(), 'lxml')
# soup = str(soup)

res = []

tags = [tag.get_text().strip() for tag in soup.select('div[class="c_container allmakes"]')[0].findAll('a')]

for tag in tags[0:1]:
    print(tag)

    # tag = tags[0]
    url = f'{url_ini}/{tag}'

    url = url.replace(' ', '%20')

    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response.read(), 'lxml')
    # soup = str(soup)

    cats = [cat.get_text().strip() for cat in soup.select('div[class="c_container allmakes allcategories"]')[0].findAll('a')]


    for cat in cats[0:1]:
        print(cat)
        # cat = cats[0]
        url = f'{url_ini}/{tag}/{cat}'

        url = url.replace(' ', '%20')

        req = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(req)
        soup = BeautifulSoup(response.read(), 'lxml')
        # soup = str(soup)

        models = [model.get_text().strip() for model in soup.select('div[class="c_container allmodels"]')[0].findAll('a')]


        for model in models[0:1]:
            print(model)

            # model = models[0]
            url = f'{url_ini}/{tag}/{cat}/{model}'

            url = url.replace(' ', '%20')

            req = urllib.request.Request(url, headers=hdr)
            response = urllib.request.urlopen(req)
            soup = BeautifulSoup(response.read(), 'lxml')
            # soup = str(soup)

            parts = [part.get_text().strip() for part in soup.select('div[class="c_container allparts"]')[0].findAll('a')]
            res.append([tag, cat, model, parts])

import pandas as pd
import numpy as np

df =  pd.DataFrame(index = pd.MultiIndex.from_product([[tag],[cat], [model], parts])).reset_index()
splitting = lambda x: x.split(' - ')
columns = ['manufactrer', 'category', 'model', 'part', 'part_category']

df.loc[:,'part'] = None
df.loc[:,'part_category'] = None
df.loc[:,['part', 'part_category']] = df.level_3.apply(splitting)
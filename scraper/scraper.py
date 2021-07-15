import urllib.request
from bs4 import BeautifulSoup
import mysql.connector
import time
import logging

print('Initiating SQL connection after DB is deployed')

time.sleep(10)

config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'urparts_scraper'
    }

connection = mysql.connector.connect(**config)

print("Connection opened, started scraping")
url_ini = 'https://www.urparts.com/index.cfm/page/catalogue'
hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }

div_levels = {1: 'div[class="c_container allmakes"]',
              2: 'div[class="c_container allmakes allcategories"]',
              3: 'div[class="c_container allmodels"]',
              4: 'div[class="c_container allparts"]'}



def extract_lower_data(url : str, tag : str, level : int):
    """Gets and prints the spreadsheet's header columns

    Parameters
    ----------
    file_loc : str
        The file location of the spreadsheet
    print_cols : bool, optional
        A flag used to print the columns to the console (default is
        False)

    Returns
    -------
    list
        a list of strings used that are the header columns
    """

    print(f'Scraping {tag} {level} level out of 4')

    if level >1: url = f'{url}/{tag}'

    url = url.replace(' ', '%20')
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response.read(), 'lxml')
    try:
        lower_tags = [cat.get_text().strip() for cat in
                      soup.select(div_levels[level])[0].findAll('a')]
        if level == 4:
            manufacturer = url.split('/')[6].strip().replace('%20', '')
            category = url.split('/')[7].strip().replace('%20', '')
            model = url.split('/')[8].strip().replace('%20', '')
            parts = [part.strip().split(' - ') for part in lower_tags]
            return res.extend([(manufacturer, category, model, part[0], part[1]) for part in parts])
    except IndexError:
        print("No data found")
        return
    return lower_tags, url


def write_to_mysql(output):
    """Gets and prints the spreadsheet's header columns

    Parameters
    ----------
    file_loc : str
        The file location of the spreadsheet
    print_cols : bool, optional
        A flag used to print the columns to the console (default is
        False)

    Returns
    -------
    list
        a list of strings used that are the header columns
    """
    db_cursor = connection.cursor()
    sql_statement = "INSERT INTO urparts_scraper.parts (manufacturer, category, model, part, part_category) values(%s, %s, %s, %s, %s)"
    db_cursor.executemany(sql_statement, list(output))
    try:
        connection.commit()
        print(f'Inserted {len(output)} values')
    except MySQLdb.IntegrityError:
        print("Failed to insert values")



if __name__ == '__main__':

    tags, url = extract_lower_data(url_ini, tag = '', level = 1)

    for tag in tags:
        res = []
        cats, url_2 = extract_lower_data(url_ini, tag =  tag, level = 2)

        for cat in cats:
            models, url_3 = extract_lower_data(url_2, tag = cat, level = 3)

            for model in models:
                extract_lower_data(url_3 ,tag = model, level = 4)

        print('Writing into MySQL Database')
        write_to_mysql(res)
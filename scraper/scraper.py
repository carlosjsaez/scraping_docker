import urllib.request
from bs4 import BeautifulSoup
import mysql.connector


# Config files

config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'urparts_scraper'
    }

url_ini = 'https://www.urparts.com/index.cfm/page/catalogue'
hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }

div_levels = {1: 'div[class="c_container allmakes"]',
              2: 'div[class="c_container allmakes allcategories"]',
              3: 'div[class="c_container allmodels"]',
              4: 'div[class="c_container allparts"]'}

# Functions definition

def extract_lower_data(url : str, tag : str, level : int):
    """Extract lower level data from the website

    Parameters
    ----------
    url : str
        previously scraped url
    tag : str
        tag of the product which we want to extract information
    level : int
        level of the product, an artificial variable which will help to navigate

    Returns
    -------
    lower_tags : list
        a list of strings returned by the website
    url : str
        url scraped
    """

    print(f'Scraping {tag} {level} level out of 4')

    # Read the website with the tag provided. We will store the tags we are looking for thanks to the level provided
    if level > 1: url = f'{url}/{tag}'
    url = url.replace(' ', '%20')
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response.read(), 'lxml')

    # In case there is data, return it with the URL or handle it in case it is from the deeper level
    try:
        lower_tags = [cat.get_text().strip() for cat in
                      soup.select(div_levels[level])[0].findAll('a')]

        # If this is the deeper level, we do not want to return any data, but to update the results list
        if level == 4:

            # We will define the output thanks to the current URL and by splitting the lower level tags
            manufacturer = url.split('/')[6].strip().replace('%20', '')
            category = url.split('/')[7].strip().replace('%20', '')
            model = url.split('/')[8].strip().replace('%20', '')
            parts = [part.strip().split(' - ') for part in lower_tags]
            return res.extend([(manufacturer, category, model, part[0], part[1]) for part in parts])
    except IndexError:

        # In case there is no data, skip the tag
        print("No data found")
        return

    return lower_tags, url


def write_to_mysql(output):
    """Writes the results of the scraping to the SQL database

    Parameters
    ----------
    output : list
        list of tuples that will be written in the database

    """
    try:
        print('Initiating SQL connection after DB is deployed')

        # Opens and closes the connection for in every writing
        connection = mysql.connector.connect(**config)

        db_cursor = connection.cursor()
        sql_statement = "INSERT INTO urparts_scraper.parts (manufacturer, category, model, part, part_category) values(%s, %s, %s, %s, %s)"
        db_cursor.executemany(sql_statement, list(output))

        connection.commit()
        print(f'Inserted {len(output)} values')
        connection.close()

    except:
        print("Something went wrong, please check the logs")


if __name__ == '__main__':

    # Reading of the higher level of the website
    tags, url = extract_lower_data(url_ini, tag = '', level = 1)

    # Loop over the subsequent levels
    for tag in tags:

        # Gather the results in res, as we want to write for every manufacturer
        res = []
        cats, url_2 = extract_lower_data(url_ini, tag =  tag, level = 2)

        for cat in cats:
            models, url_3 = extract_lower_data(url_2, tag = cat, level = 3)

            # This level will not return anything, but will just write in the database
            for model in models:
                extract_lower_data(url_3 ,tag = model, level = 4)

        print('Writing into MySQL Database')
        write_to_mysql(res)

    print('Whole website stored in our database')

import os, requests, json, sys
from cutlet import Cutlet
from bs4 import BeautifulSoup

print('Welcome to RemyWiki Cover scraper!')
if len(sys.argv) != 2:
    print('usage: cover_scraper <song_title>')
    sys.exit()

config_path = './config.json'
if os.path.exists(config_path):
    with open(config_path, 'r') as file:
        config = json.loads(file.read())
        config: dict
else:
    print('Can\'t find the config file!')
    sys.exit()

assets = config.get('asset_store', '')
wiki = config.get('wiki', {})
wiki_url = wiki.get('head_url', '')

song = sys.argv[1]
print(f'Scraping data for {song}')

romanize = Cutlet()
song: str = romanize.romaji(song)
song = song.replace(' ', '_')

# Start by getting the song data
page = requests.get(f'{wiki_url}{song}')
soup = BeautifulSoup(page.content, 'html.parser')

# Find cover photos in data
covers = []
tables = soup.find_all('a', {"class": "image"})
for table in tables:
    covers.append(table['href'].replace('/', ''))

# Using the covers, scrape the `File:` pages for the full-size art.
for index, cover in enumerate(covers):
    page = requests.get(f'{wiki_url}{cover}')
    soup = BeautifulSoup(page.content, 'html.parser')
    image_div = soup.find('div', {"class": "fullImageLink"})
    image = image_div.find('a')
    if image != None:
        img_src = image['href']
        texture = requests.get(f'{wiki_url}{img_src}')
        if os.path.exists(assets):
            with open(f'{assets}{song}_{index}.png', 'wb') as png_file:
                png_file.write(texture.content)
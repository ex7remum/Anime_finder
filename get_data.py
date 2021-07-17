import requests
from bs4 import BeautifulSoup
import pandas as pd

anime_titles = []
anime_ids = []
anime_genres = []
MAX_ID = 24501
all_genres = set()

for i in range(1, MAX_ID):
    url = f'https://cdn.animenewsnetwork.com/encyclopedia/api.xml?anime={i}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        title = soup.find_all(type="Main title")[0].text
        anime_genres_block = soup.find_all(type="Genres")
        for genre in anime_genres_block:
            all_genres.add(genre)
        cur_genres = [genre.text.lower() for genre in anime_genres_block]
        anime_titles.append(title)
        anime_ids.append(i)
        anime_genres.append(cur_genres)
    except:
        continue

df = pd.DataFrame(
    {
        'anime_titles': anime_titles,
        'anime_ids': anime_ids,
        'anime_genres': anime_genres,
    }
)

df.to_csv('full_anime_list.csv', encoding='utf-8', index=False)
#df = pd.read_csv('full_anime_list.csv')
#print(all_genres)
#print(df.head())

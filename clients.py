import urllib.request
import requests
import random
from bs4 import BeautifulSoup
import pandas as pd
from typing import Dict, List


def CreateTextById(anime_id: int, anime_title: str) -> Dict[str, str]:
    POST_URL = "https://cdn.animenewsnetwork.com/encyclopedia" \
               "/api.xml?anime={}".format(anime_id)
    try:
        response = requests.get(POST_URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        plot = soup.find_all(type="Plot Summary")
        picture_link = soup.find_all(type="Picture")[0]['src']
        rating = soup.find_all("ratings")[0]["weighted_score"]
        anime_description = plot[0].text
        return {
            "message": "ok",
            "picture": picture_link,
            "title": anime_title,
            "description": anime_description,
            "rating": rating
        }
    except:
        return {
            "message": "Error occured, please try again later."
        }


class FindAnimeByGenres:
    SORRY_MESSAGE = "Sorry, we haven't found suitable anime."
    ERROR_MESSAGE = "Error occured, please try again later."

    def __init__(self):
        self._data = pd.read_csv('full_anime_list.csv')

    def __call__(
            self,
            need_genres: List[str]
    ) -> Dict[str, str]:

        indexes_match_queries = self._data.apply(
            lambda row: sum([genre in row['anime_genres']
                             for genre in need_genres]) == len(need_genres),
            axis=1,
        )

        found_anime = self._data[indexes_match_queries]

        if len(found_anime) == 0:
            return {
                "message": self.SORRY_MESSAGE,
            }

        index = random.randint(0, len(found_anime) - 1)
        anime_id = found_anime.iloc[index]["anime_ids"]
        anime_title = found_anime.iloc[index]["anime_titles"]
        try:
            return CreateTextById(anime_id, anime_title)
        except:
            return {
                "message": self.ERROR_MESSAGE,
            }


class FindAnimeByURL:
    POST_URL = "https://api.trace.moe/search?anilistInfo&url={}"
    SORRY_MESSAGE = "Sorry, we haven't found suitable anime."
    ERROR_MESSAGE = "Error occured, please try again later."

    def __init__(self):
        self._data = pd.read_csv('full_anime_list.csv')

    def __call__(
            self,
            picture_url: str
    ) -> Dict[str, str]:

        if "https://" not in picture_url:
            picture_url = "https://" + picture_url

        try:
            anime_id = -1
            request = requests.get(self.POST_URL.format(
                urllib.parse.quote_plus(picture_url))).json()
            if len(request["result"]) == 0:
                return{
                    "message": self.SORRY_MESSAGE,
                }

            anime_title = request["result"][0]['anilist']['title']['romaji']

            for language in request["result"][0]['anilist']['title']:
                title = request["result"][0]['anilist']['title'][language]
                if self._data[self._data.anime_titles == title].count()[0] > 0:
                    anime_id = self._data[self._data.anime_titles ==
                                          title].iloc[0]["anime_ids"]
                    anime_title = title
                    break

            if anime_id == -1:
                return {
                    "message": "ok",
                    "picture": "",
                    "title": anime_title,
                    "description": "Not found this anime in database.",
                    "rating": "Unknown"
                }
            else:
                return CreateTextById(anime_id, anime_title)
        except:
            return {
                "message": self.ERROR_MESSAGE
            }

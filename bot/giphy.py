import requests
import random


def get_random_gif_url(category, giphy_key):
    random_index = random.randint(0, 24)
    params = {"api_key": giphy_key, "q": category, "rating": "g"}
    url = "https://api.giphy.com/v1/gifs/search"
    r = requests.get(url, params)
    gifs_json = r.json()
    gif_url = gifs_json["data"][random_index]["images"]["downsized"]["url"]
    return gif_url

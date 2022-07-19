import pandas as pd
import requests
import random
import sqlalchemy as db


def genre(): 
    genre = input("Enter genre:")
    return genre

def get_games(genre):
    genre = genre()
    url = "https://www.freetogame.com/api/games?category={}".format(genre)
    games = requests.get(url)
    games_data = games.json()
    title_list = []
    thumbnail_list = []
    description_list = []
    url_list = []
    for game in games_data:
        title_list.append(game['title'])
        thumbnail_list.append(game['thumbnail'])
        description_list.append(game['short_description'])
        url_list.append(game['game_url'])

    games_df = pd.DataFrame(list(zip(title_list, thumbnail_list, description_list, url_list)),
               columns =['Title', 'Image', 'Description', 'Link'])
    
    print(games_df.sample(n=3))


get_games(genre)




     




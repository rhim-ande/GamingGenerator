import pandas as pd
import requests
import random
import sqlalchemy as db


def genre(): 
    genre = input("Enter genre:")
    return genre

def get_games(genre):
    url = "https://www.freetogame.com/api/games?category={}".format(genre)
    games = requests.get(url)
    games_data = games.json()
    title_list = []
    thumbnail_list = []
    description_list = []
    url_list = []
    total_games = []
    for game in games_data:
        title_list.append(game['title'])
        thumbnail_list.append(game['thumbnail'])
        description_list.append(game['short_description'])
        url_list.append(game['game_url'])
        total_games.append([game['title'], game['thumbnail'], game['short_description'], game['game_url']])

    return random.choices(total_games, k=3)
    #games_df = pd.DataFrame(list(zip(title_list, thumbnail_list, description_list, url_list)),
               #columns =['Title', 'Image', 'Description', 'Link'])
    
    #return title_list
    #games_df.sample(n=3)


#get_games(genre)




     




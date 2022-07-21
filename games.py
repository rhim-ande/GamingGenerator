import requests
import random


def genre(): 
    genre = input("Enter genre:")
    return genre

def get_games(genre):
    url = "https://www.freetogame.com/api/games?category={}".format(genre)
    games = requests.get(url)
    games_data = games.json()
    total_games = []
    for game in games_data:
        total_games.append([game['title'], game['thumbnail'], game['short_description'], game['game_url']])

    return random.choices(total_games, k=3)



     




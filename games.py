import requests
import random

def get_games(genre):
    url = "https://www.freetogame.com/api/games?category={}".format(genre)
    games = requests.get(url)

    games_data = games.json()
    total_games = []
    for game in games_data:
        total_games.append([game['title'], game['thumbnail'], game['short_description'], game['game_url']])

    results = random.choices(total_games, k=3)
    for game in results:
        if results.count(game) > 1:
            game = random.choice(total_games)

    return results

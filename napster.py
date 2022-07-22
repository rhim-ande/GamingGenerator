import requests
import json
import random
 

def short_to_id(shortcut):
    if shortcut == 'rock':
        return 'g.5'
    elif shortcut == 'pop':
        return 'g.115'
    elif shortcut == 'alt-punk':
        return 'g.33'
    elif shortcut == 'rap-hip-hop':
        return 'g.146'
    elif shortcut == 'jazz':
        return 'g.299'
    elif shortcut == 'country':
        return 'g.407'
    elif shortcut == 'electronica-dance':
        return 'g.71'
    elif shortcut == 'latin':
        return 'g.510'
    elif shortcut == 'metal':
        return 'g.394'
    elif shortcut == 'classical':
        return 'g.21'
    elif shortcut == 'soul-r-and-b':
        return 'g.194'
    elif shortcut == 'new-age':
        return 'g.453'
    elif shortcut == 'reggae':
        return 'g.383'
    elif shortcut == 'blues':
        return 'g.438'
    elif shortcut == 'christian-gospel':
        return 'g.75'
    elif shortcut == 'folk':
        return 'g.446'
    elif shortcut == 'children':
        return 'g.470'
    elif shortcut == 'vocal-easy-listening':
        return 'g.69'
    elif shortcut == 'soundtracks-musicals':
        return 'g.246'
    elif shortcut == 'comedy-spoken-word':
        return 'g.156'
    else:
        return 'sorry genre not available'
 
 
#getting list of the top artist and album names per genre
def get_albs(genre):
    complete_list = []
    albs = requests.get('http://api.napster.com/v2.2/genres/'+genre+'/albums/top?apikey=Zjk1NzYyNGEtMDVjNi00MGI5LTlhZGItOTA1MjVlNTg5NDE4').json()
    for i in range(len(albs['albums'])):
        complete_list.append([albs['albums'][i]['name'], albs['albums'][i]['artistName']])
    return complete_list

#getting a random album from the list we have generated
def random_album(albums):
    the_one = random.choice(albums)
    return the_one

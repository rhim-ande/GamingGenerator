import requests
import pandas as pd
import json
import sqlalchemy as db
import pprint
import random
 
 
#gene= requests.get('http://api.napster.com/v2.2/genres?apikey=Zjk1NzYyNGEtMDVjNi00MGI5LTlhZGItOTA1MjVlNTg5NDE4').json()
#albs = requests.get('http://api.napster.com/v2.2/genres//albums/top?apikey=Zjk1NzYyNGEtMDVjNi00MGI5LTlhZGItOTA1MjVlNTg5NDE4&limit=3').json()
 
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
    elif shortcut == 'reaggae':
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
    complete_list=[]
    albs = requests.get('http://api.napster.com/v2.2/genres/'+genre+'/albums/top?apikey=Zjk1NzYyNGEtMDVjNi00MGI5LTlhZGItOTA1MjVlNTg5NDE4').json()
    for i in range(len(albs['albums'])):
        complete_list.append([albs['albums'][i]['name'], albs['albums'][i]['artistName']])
    return complete_list
 
 
#listing the shortcuts used for the genres
def list_genres(response):
    genre_list=[]
    for i in range(len(response['genres'])):
        genre_list.append(response['genres'][i]['shortcut'])
    return genre_list
 
#getting a random album from the list we have generated
def random_album(albums):
    the_one = random.choice(albums)
    print(the_one)
 
#putting the info into a dataframe
def album_dataframe(title):
    column_names = ['Album Titles']
    data= {'Album':[title]}
    album_df= pd.DataFrame(data)
    engine = db.create_engine('sqlite:///album_names.db')
    album_df.to_sql('data', con=engine, if_exists='replace', index=False)
    return pd.DataFrame(engine.execute("SELECT * FROM data;").fetchall(), columns = column_names)
 
#genres= list_genres(gene)
#print('list of genres available:')
#print(genres)
 
#genre= input('please enter a genre: ')
#genre_id= short_to_id(genre)
#albums= get_albs(genre_id)
#al= random_album(albums)
#print(album_dataframe(al))

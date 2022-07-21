# GamingGenerator
> A websebite used to generate a random list of free to play based on genre,
> as well as generate one album based on a list of the top albums per genre
## This website is made using the napster and freetogame api's
* As napster is used with the genre top albums endpoint
  * this is done by having the user input the name of a genre which is then turned into a genre id
  * This pulls up a list of the top albums of the chosen genre 
  * which is looked through by a random function which returns one random from the list
* Similarly freetogame is used with the search by category endpoint
  * where user input is used to pull a list of games based on genre
  * that list is then put through a random function which picks 3 games
### here are the requirements that were used in the creation of this website
* click v8.0.1
* Flask v2.0.1
* gunicorn v20.0.4
* itsdangerous v2.0.1
* Jinja2 V3.0.1
* MarkupSafe v2.0.1
* Werkzeug v2.0.1
* Flask-WTF v0.15.1
* email_validator v1.1.3
* flask_behind_proxy v0.1.1
* flask_sqlalchemy
* pytest
* pycodestyle
* requests
* flask_login

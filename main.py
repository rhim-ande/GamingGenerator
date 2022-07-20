from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, GameForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from games import get_games
from napster import short_to_id, get_albs, random_album

app = Flask(__name__)
proxied = FlaskBehindProxy(app) 

app.config['SECRET_KEY'] = '78de1af656d14fd39ee8e9ca98fd5989'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/myaccount", methods=['GET', 'POST'])
def myaccount():
    return render_template('myaccount.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #pw = #query for password
        #check user is in database and password correct 
        if user is None:
            return render_template('login.html', title='Login', form=form)
        flash(f'Successful login {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('login.html', title='Login', form=form)

@app.route("/get_game", methods=['GET', 'POST'])
def get_game():
    form = GameForm()
    return render_template('getgame.html', title='GetGame', form=form)

@app.route("/results", methods=['GET', 'POST'])
def results():
    form = GameForm()
    id_number = short_to_id(form.music_genre.data)
    album_list = get_albs(id_number)
    album = random_album(album_list)
    games = get_games(form.game_genre.data)
    return render_template('results.html', d1=f'{games[0][2]}', d2=f'{games[1][2]}', d3=f'{games[2][2]}',link1=f'{games[0][3]}', link2=f'{games[1][3]}', link3=f'{games[2][3]}', game1 = f'{games[0][0]}', game2 = f'{games[1][0]}', game3 = f'{games[2][0]}', img1 = f'{games[0][1]}', img2 = f'{games[1][1]}',img3 = f'{games[2][1]}', album = f'{album}', title='Results')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
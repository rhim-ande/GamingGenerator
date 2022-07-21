from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, GameForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from games import get_games
from napster import short_to_id, get_albs, random_album
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
proxied = FlaskBehindProxy(app) 

app.config['SECRET_KEY'] = '78de1af656d14fd39ee8e9ca98fd5989'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    game1 = db.Column(db.String(), nullable=False)
    game2 = db.Column(db.String(), nullable=False)
    game3 = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Games('{self.username}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/myaccount", methods=['GET', 'POST'])
@login_required
def myaccount():
    user_games = Games.query.filter_by(username=current_user.username).first()
    if user_games.game3 != " ":
        game3_info = user_games.game3.split(', ')
        game2_info = user_games.game2.split(', ')
        game1_info = user_games.game1.split(', ')
        return render_template('myaccount.html', d1=f'{game1_info[2]}', d2=f'{game2_info[2]}', d3=f'{game3_info[2]}',link1=f'{game1_info[3]}', link2=f'{game2_info[3]}', link3=f'{game3_info[3]}', game1 = f'{game1_info[0]}', game2 = f'{game2_info[0]}', game3 = f'{game3_info[0]}', img1 = f'{game1_info[1]}', img2 = f'{game2_info[1]}', img3 = f'{game3_info[1]}', title='Results')
    return render_template('myaccount.html', name=current_user.username)

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    name = current_user.username
    logout_user()
    return render_template('logout.html', name=name)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        if User.query.filter_by(email=form.email.data).first():
            flash('This email is already associated with an account')
            return redirect(url_for('register'))
        user = User(username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data, method='pbkdf2:sha256'))
        user_games = Games(username=form.username.data, game1=" ", game2=" ", game3=" ")
        db.session.add(user)
        db.session.commit()
        db.session.add(user_games)
        db.session.commit()
        flash(f'Account created for {form.username.data}, please login!', 'success')
        return redirect(url_for('login')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not check_password_hash(user.password, form.password.data):
           flash('Username or password incorrect, please try again.')
           return redirect(url_for('login'))
        flash(f'Successful login {form.username.data}!', 'success')
        login_user(user, remember=True)
        return redirect(url_for('myaccount')) # if so - send to home page
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
    user_games = Games.query.filter_by(username=current_user.username).first()
    user_games.game1 = ', '.join(games[0])
    user_games.game2 = ', '.join(games[1])
    user_games.game3 = ', '.join(games[2]) 
    db.session.commit()
    return render_template('results.html', d1=f'{games[0][2]}', d2=f'{games[1][2]}', d3=f'{games[2][2]}',link1=f'{games[0][3]}', link2=f'{games[1][3]}', link3=f'{games[2][3]}', game1 = f'{games[0][0]}', game2 = f'{games[1][0]}', game3 = f'{games[2][0]}', img1 = f'{games[0][1]}', img2 = f'{games[1][1]}',img3 = f'{games[2][1]}', albumName = f'{album[0]}', albumArtist = f'{album[1]}', title='Results')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
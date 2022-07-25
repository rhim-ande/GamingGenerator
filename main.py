from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, GameForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from games import get_games
from napster import short_to_id, get_albs, random_album
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user
from flask_login import LoginManager, login_required, current_user, logout_user
import requests

app = Flask(__name__)
proxied = FlaskBehindProxy(app)

app.config['SECRET_KEY'] = '78de1af656d14fd39ee8e9ca98fd5989'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

#initialize login manager for registration and login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def has_game1(self):
        '''check that a user has a game in the game1 section of database'''
        user_games = Games.query.filter_by(username=self.username).first()
        game1_info = user_games.game1.split(', ')
        if user_games.game1 is " ":
            return False
        return True

    def has_game2(self):
        '''check that a user has a game in the game2 section of database'''
        user_games = Games.query.filter_by(username=self.username).first()
        game2_info = user_games.game2.split(', ')
        if user_games.game2 == " ":
            return False
        return True

    def has_game3(self):
        '''check that a user has a game in the game3 section of database'''
        user_games = Games.query.filter_by(username=self.username).first()
        game3_info = user_games.game3.split(', ')
        if user_games.game3 == " ":
            return False
        return True

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    game1 = db.Column(db.String(), nullable=False)
    game2 = db.Column(db.String(), nullable=False)
    game3 = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Games('{self.username}, '{self.game1}')"


@app.route("/get_url_game", methods=['GET', 'POST'])
@login_required
def get_url_game():
    '''get url to send user to gaming site'''
    variable = request.args.get('variable')
    variable = variable.split(', ')

    url = variable[3]
    if variable[4] == '1':
        variable = ', '.join(variable)
        user_games = Games.query.filter_by(username=current_user.
                                           username).first()
        user_games.game1 = variable
    if variable[4] == '2':
        variable = ', '.join(variable)
        user_games = Games.query.filter_by(username=current_user.
                                           username).first()
        user_games.game2 = variable
    if variable[4] == '3':
        variable = ', '.join(variable)
        user_games = Games.query.filter_by(username=current_user.
                                           username).first()
        user_games.game3 = variable
    db.session.commit()

    return redirect(url)


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
    '''myaccount page to display user history'''
    user_games = Games.query.filter_by(username=current_user.username).first()
    if user_games.game3 != " ":
        game3_info = user_games.game3.split(', ')
        game2_info = user_games.game2.split(', ')
        game1_info = user_games.game1.split(', ')
        return render_template('myaccount.html',
                               d1=f'{game1_info[2]}', d2=f'{game2_info[2]}',
                               d3=f'{game3_info[2]}', link1=f'{game1_info[3]}',
                               link2=f'{game2_info[3]}',
                               link3=f'{game3_info[3]}',
                               game1=f'{game1_info[0]}',
                               game2=f'{game2_info[0]}',
                               game3=f'{game3_info[0]}',
                               img1=f'{game1_info[1]}',
                               img2=f'{game2_info[1]}',
                               img3=f'{game3_info[1]}',
                               title='Results')
    if user_games.game2 != " ":
        game2_info = user_games.game2.split(', ')
        game1_info = user_games.game1.split(', ')
        return render_template('myaccount.html',
                               d1=f'{game1_info[2]}', d2=f'{game2_info[2]}',
                               link1=f'{game1_info[3]}',
                               link2=f'{game2_info[3]}',
                               game1=f'{game1_info[0]}',
                               game2=f'{game2_info[0]}',
                               img1=f'{game1_info[1]}',
                               img2=f'{game2_info[1]}',
                               title='Results')
    if user_games.game1 != " ":
        game1_info = user_games.game1.split(', ')
        return render_template('myaccount.html',
                               d1=f'{game1_info[2]}',
                               link1=f'{game1_info[3]}',
                               game1=f'{game1_info[0]}',
                               img1=f'{game1_info[1]}',
                               title='Results')
    return render_template('myaccount.html')


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    name = current_user.username
    logout_user()
    return render_template('logout.html', name=name)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('This email is already associated with an account', 'error')
            return redirect(url_for('register'))
        user = User(username=form.username.data, email=form.email.data,
                    password=generate_password_hash(form.password.data,
                                                    method='pbkdf2:sha256'))
        user_games = Games(username=form.username.data,
                           game1=" ", game2=" ", game3=" ")
        db.session.add(user)
        db.session.commit()
        db.session.add(user_games)
        db.session.commit()
        flash(f'Account created for {form.username.data},' +
              'please login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not check_password_hash(user.password,
                                               form.password.data):
            flash('Username or password incorrect,' +
                  'please try again.', category='error')
            return redirect(url_for('login'))
        flash(f'Successful login {form.username.data}!', 'success')
        login_user(user, remember=True)
        return redirect(url_for('myaccount'))
    return render_template('login.html', title='Login', form=form)


@app.route("/get_game", methods=['GET', 'POST'])
def get_game():
    form = GameForm()
    return render_template('getgame.html', title='GetGame', form=form)


@app.route("/results", methods=['GET', 'POST'])
def results():
    '''page to show results of user choices'''
    form = GameForm()
    id_number = short_to_id(form.music_genre.data)
    album_list = get_albs(id_number)
    album = random_album(album_list)
    games = get_games(form.game_genre.data)

    #attempt to check status code of get request and take out bad links
    response1 = requests.get(games[0][3])
    response2 = requests.get(games[1][3])
    response3 = requests.get(games[2][3])
    showLink1 = "True" if response1.status_code != 404 else "False"
    showLink2 = "True" if response2.status_code != 404 else "False"
    showLink3 = "True" if response3.status_code != 404 else "False"

    return render_template('results.html', showLink1=showLink1,
                           showLink2=showLink2, showLink3=showLink3,
                           d1=f'{games[0][2]}', d2=f'{games[1][2]}',
                           d3=f'{games[2][2]}',
                           link1=f'{games[0][3]}',
                           link2=f'{games[1][3]}',
                           link3=f'{games[2][3]}',
                           game1=f'{games[0][0]}',
                           game2=f'{games[1][0]}',
                           game3=f'{games[2][0]}',
                           img1=f'{games[0][1]}',
                           img2=f'{games[1][1]}',
                           img3=f'{games[2][1]}',
                           albumName=f'{album[0]}',
                           albumArtist=f'{album[1]}',
                           title='Results')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

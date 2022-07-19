from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, GameForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line

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
    if form.validate_on_submit(): # checks if entries are valid
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
    return render_template('results.html', title='Results')



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


from flask_login import current_user, login_user, logout_user, login_required
from .forms import LoginForm
from flask import render_template, flash, redirect
from .models import User


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Эльдар Рязанов'}
    posts = []
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
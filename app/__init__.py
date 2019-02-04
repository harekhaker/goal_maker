from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import request

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
from werkzeug.urls import url_parse


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username.data).first()
        user.get_id()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        id = user.get_id()
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = '/page?id=%s'%id
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/page')
@login_required
def index():

    posts = []
    return render_template('index.html', title='Home',  posts=posts)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
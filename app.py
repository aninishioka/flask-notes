import os
from models import db, User
from flask import Flask, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///playlist_app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config["SECRET_KEY"] = 'letterboxd'

@app.get('/')
def display_homepage():
    return redirect('/register')


@app.route('/regiser', methods = ["GET", "POST"])
def display_register():
    form = RegisterForm()


    if form.validate_on_submit():
        username =form.username.data
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register_user(username=username, email=email,
                password=password, first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()

        session['user'] = user.username

        return redirect(f'/users/{user.username}')

    return render_template('register.html', form=form)

@app.get('/user/<username>')
def display_user_profile(username):
    if session['user'] and username == session['user']:
        user = User.query.get_or_404(username)
        return render_template('user.html', user=user)

    else:
        # TODO: flash message
        return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def display_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.get(form.username.data)




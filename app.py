import os
from models import db, User
from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm

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

        user = User(username=username, email=email, password=password,
                    first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()

        return redirect('/users/username')

    return render_template('base.html', form=form)


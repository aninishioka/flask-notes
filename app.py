import os
from models import db, User, connect_db
from flask import Flask, redirect, render_template, session
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///notes_app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config["SECRET_KEY"] = 'letterboxd'

connect_db(app)

# TODO: constant session user key

@app.get('/')
def display_homepage():
    """Displays homepage"""

    return redirect('/register')


@app.route('/register', methods = ["GET", "POST"])
def register():
    """If form validates, creates new user
    and logs user in. Else, dispalys form."""

    if session.get('user'):
        return redirect(f'/users/{session["user"]}')

    form = RegisterForm()


    if form.validate_on_submit():
        username =form.username.data
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name)

        db.session.add(user)
        db.session.commit()

        session['user'] = user.username

        return redirect(f'/users/{user.username}')

    return render_template('register.html', form=form)


@app.get('/users/<username>')
def display_user_profile(username):
    """Displays user profile if logged in. Else, redirect to homepage."""

    form = CSRFProtectForm()

    if session.get('user') and username == session['user']:
        user = User.query.get_or_404(username)
        return render_template('user.html', user=user, form=form)

    else:
        # TODO: flash message
        return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """If form valid, logs in user. Else, renders form."""

    if session.get('user'):
        return redirect(f'/users/{session["user"]}')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['user'] = user.username
            return redirect(f'/users/{username}')

        else:
            form.username.errors = ['Bad username/password']

    return render_template('login.html', form=form)


@app.post('/logout')
def logout():
    """Logs out user."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop('user', None)

    return redirect('/')





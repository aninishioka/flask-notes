import os
from models import db, User, connect_db, Note
from flask import Flask, redirect, render_template, session
from forms import RegisterForm, LoginForm, CSRFProtectForm, AddNoteForm, EditNoteForm
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///notes_app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config["SECRET_KEY"] = 'letterboxd'

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
debug = DebugToolbarExtension(app)

connect_db(app)

USER_KEY = 'user'

@app.get('/')
def display_homepage():
    """Displays homepage"""

    return redirect('/register')


@app.route('/register', methods = ["GET", "POST"])
def register():
    """If form validates, creates new user
    and logs user in. Else, dispalys form."""

    if session.get(USER_KEY):
        print('****************************************HERE')
        return redirect(f'/users/{session[USER_KEY]}')

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

        session[USER_KEY] = user.username

        return redirect(f'/users/{user.username}')

    return render_template('register.html', form=form)


@app.get('/users/<username>')
def display_user_profile(username):
    """Displays user profile if logged in. Else, redirect to homepage."""

    form = CSRFProtectForm()

    if session.get(USER_KEY) and username == session[USER_KEY]:
        user = User.query.get_or_404(username)
        return render_template('user.html', user=user, form=form)

    else:
        # TODO: flash message
        # TODO: redirect to login
        return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """If form valid, logs in user. Else, renders form."""

    if session.get(USER_KEY):
        return redirect(f'/users/{session[USER_KEY]}')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session[USER_KEY] = user.username
            return redirect(f'/users/{username}')

        else:
            form.username.errors = ['Bad username/password']

    return render_template('login.html', form=form)


@app.post('/logout')
def logout():
    """Logs out user."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop(USER_KEY, None)

    return redirect('/')


########### USER SPECIFIC ROUTES ###################

@app.post('/users/<username>/delete')
def delete_user(username):
    """Deletes user."""
    form = CSRFProtectForm()
    user = User.query.get_or_404(username)

# TODO: move to top of func
    if not (USER_KEY in session and session[USER_KEY] == username):
        return redirect('/')


    if form.validate_on_submit():
        # not N+1 !!
        notes = Note.query.filter(Note.owner_username == user.username)

        for note in notes:
            db.session.delete(note)

        db.session.delete(user)
        db.session.commit()

        session.pop(USER_KEY, None)

        return redirect('/')
    else:
        # TODO:
        render_template('user.html', user=user, form=form)

@app.route('/users/<username>/notes/add', methods = ['POST', 'GET'])
def add_note(username):

    """if GET, show form to add a note,
    if POST, handle form data and add note"""

    if not (USER_KEY in session and session[USER_KEY] == username):
        return redirect('/')

    form = AddNoteForm()

    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            content=form.content.data,
            owner_username=username
        )
        db.session.add(note)
        db.session.commit()

        return redirect(f'/users/{username}')

    else:
        # render add note form
        return render_template('add_note.html', form=form)


@app.route('/notes/<note_id>/update', methods = ['GET', 'POST'])
def edit_note(note_id):
    """If form valid, edits note. Else, renders edit note form"""

    note = Note.query.get_or_404(note_id)

# TODO: match other auth
    if session.get(USER_KEY) != note.owner_username:
        return redirect('/')

    form = EditNoteForm(obj=note)

    if form.validate_on_submit():
        title = form.title.data or note.title
        content = form.content.data or note.content

        note.title = title
        note.content = content

        db.session.commit()

        return redirect(f'/users/{note.owner_username}')

    else:
        return render_template('edit_note.html', form=form)


@app.post('/notes/<note_id>/delete')
def delete_note(note_id):
    """Deletes note. Redirects to user page"""

    note = Note.query.get_or_404(note_id)

# match others
    if session.get(USER_KEY) != note.owner_username:
        return redirect('/')

    form = CSRFProtectForm()

    if form.validate_on_submit():

        db.session.delete(note)
        db.session.commit()

        # TODO: flash message
        return redirect(f'/users/{note.owner_username}')

    else:
        # TODO: kick them out














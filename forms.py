from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length

# TODO: email validator
class RegisterForm(FlaskForm):
    """form for registering user"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=20)]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(max=30)]
    )

    email = EmailField(
        "Email",
        validators=[InputRequired(),Length(max=50)]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired(),Length(max=30)]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(),Length(max=30)]
    )


class LoginForm(FlaskForm):
    """form for signing in user"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])


class AddNoteForm(FlaskForm):
    """Add a note form"""

    title = StringField(
        "Title",
        validators=[InputRequired(),Length(max=30)]
    )

    content = TextAreaField("Content",
        validators=[InputRequired()]
    )

# TODO: match length max with models
class EditNoteForm(FlaskForm):
    """Edit a note form"""

    title = StringField(
        "Title",
        validators=[InputRequired(),Length(max=30)]
    )

    content = TextAreaField("Content",
        validators=[InputRequired()]
    )

class CSRFProtectForm(FlaskForm):
    """For protection purposes, for logout"""

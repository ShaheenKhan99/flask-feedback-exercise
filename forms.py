from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, Optional


class CreateUserForm(FlaskForm):
    """ Form for creating new user"""
    username = StringField("Username", validators=[InputRequired(), Length(min=6, max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Length(min=6, max=50)])
    first_name = StringField("First name", validators=[InputRequired(), Length(min=2, max=30)])
    last_name = StringField("Last name", validators=[InputRequired(), Length(min=2, max=30)])


class LoginForm(FlaskForm):
    """ Form for logging in existing user"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    """ Form for creating new feedback"""

    title = StringField("Title", validators=[InputRequired(), Length(min=2, max=100)])
    content = TextAreaField("Content", validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """ Form for creating new feedback"""



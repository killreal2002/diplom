from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.user.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Remember me', default=True, render_kw={"class": "form-check-input"})
    submit = SubmitField('Submit', render_kw={'class': "btn btn-primary"})



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('User email', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    password = PasswordField('Enter password', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Submit', render_kw={'class': "btn btn-primary"})
    
    def validate_username(self, username):
        user_count = User.query.filter_by(username=username.data).count()
        if user_count > 0:
            raise ValidationError('User with this username already exists')
        
    def validate_email(self, email):
        user_count = User.query.filter_by(email=email.data).count()
        if user_count > 0:
            raise ValidationError('User with this email already exists')
    
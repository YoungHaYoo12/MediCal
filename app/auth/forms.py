from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, 
SubmitField,SelectField)
from wtforms.validators import DataRequired, EqualTo, Email, Length
from wtforms import ValidationError
from app.models import User

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(message='Email Field Empty'),
          Email(message='Email Format Not Correct'), Length(1,64)])
  password = PasswordField('Password', validators= [DataRequired(message='Password Field Empty')])
  remember_me = BooleanField('Keep Me Logged In')
  submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
  hospital = SelectField('Hospital', validators=[DataRequired(message='Hospital Field Empty')])
  first_name = StringField('First Name', validators=[DataRequired(message='First Name Field Empty')])
  last_name = StringField('Last Name', validators=[DataRequired(message='Last Name Field Empty')])  
  username = StringField('Username', validators=[DataRequired(message='Username Field Empty')])
  email = StringField('Email', validators=[DataRequired(message="Email Field Empty"), 
          Length(1,64), Email(message="Email Format Not Correct")])
  password = PasswordField('Password',validators=[DataRequired(message='Password Field Empty'), 
             EqualTo('password2',message='Passwords Must Match')])
  password2 = PasswordField('Confirm Password',validators=[DataRequired('Confirm Password Field Empty')])
  submit = SubmitField('Register')

  def validate_username(self,field):
    if User.query.filter_by(username=field.data).first():
      raise ValidationError('Username Already Taken')

  def validate_email(self,field):
    if User.query.filter_by(email=field.data).first():
      raise ValidationError('Email Already Registered')

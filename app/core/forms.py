from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class UserSearchForm(FlaskForm):
  username = StringField('Username')
  first_name = StringField('First Name')
  last_name = StringField('Last Name')
  submit = SubmitField('Search')
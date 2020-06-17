from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, DataRequired, Length

class PatientAddForm(FlaskForm):
  first_name = StringField('First Name',validators=[DataRequired(message='First Name Field Empty')])
  last_name = StringField('Last Name',validators=[DataRequired(message='Last Name Field Empty')])
  email = StringField('Email',validators=[DataRequired(message='Email Field Empty'),Email(message='Email Format Not Correct'),Length(1,64)])
  submit = SubmitField('Add Patient')

class PatientEditForm(FlaskForm):
  first_name = StringField('First Name',validators=[DataRequired(message='First Name Field Empty')])
  last_name = StringField('Last Name',validators=[DataRequired(message='Last Name Field Empty')])
  email = StringField('Email',validators=[DataRequired(message='Email Field Empty'),Email(message='Email Format Not Correct'),Length(1,64)])
  submit = SubmitField('Edit')
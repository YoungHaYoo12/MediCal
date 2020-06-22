from datetime import datetime
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField,SelectField,ValidationError
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired

class AppointmentForm(FlaskForm):
  title = StringField('Title',validators=[DataRequired(message='Title Field Empty')],default='')
  description = TextAreaField('Description',validators=[DataRequired(message='Description Field Empty')])
  date_start = DateTimeLocalField('Start Time (EDT)',validators=[DataRequired(message='Start Field Empty')],format='%Y-%m-%dT%H:%M')
  date_end = DateTimeLocalField('End Time (EDT)',validators=[DataRequired(message='End Field Empty')],format='%Y-%m-%dT%H:%M')
  treatment = SelectField('Treatment')
  patient = SelectField('Patient')
  submit = SubmitField('Submit')

  def validate(self):
    if self.date_start.data > self.date_end.data:
      raise ValidationError('Start Date Occurs Later Than End Date.')
    else:
      return True

class AppointmentFilterForm(FlaskForm):
  user = SelectField('Hospital Doctors: ')
  patient = StringField('Patient Email: ')
  treatment = StringField('Treatment: ')
  filter = SubmitField('Filter')

# SOME RULES
# HAS TO FILTER through either the current user OR their hospital OR users in their hospital

# select field choices
# patients (type in fullname)
# treatment (type in name)
# title (type in title)
# HOSPITAL DOES NOT HAVE TO BE ITS OWN FORM FIELD. IT CAN BE THE ALL OPTION!!!!!!!!!!
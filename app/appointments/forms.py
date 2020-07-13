from flask_wtf import FlaskForm
from wtforms import BooleanField,StringField, SubmitField,TextAreaField,SelectField,ValidationError,RadioField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired

class AppointmentForm(FlaskForm):
  title = StringField('Title',validators=[DataRequired(message='Title Field Empty')],default='')
  description = TextAreaField('Description',validators=[DataRequired(message='Description Field Empty')])
  date_start = DateTimeLocalField('Start Time (EDT)',validators=[DataRequired(message='Start Field Empty')],format='%Y-%m-%dT%H:%M')
  date_end = DateTimeLocalField('End Time (EDT)',validators=[DataRequired(message='End Field Empty')],format='%Y-%m-%dT%H:%M')
  treatment = SelectField('Treatment')
  patient = SelectField('Patient')
  color = RadioField('Color', choices=[('blue','Blue'),('green','Green'),('red','Red'),('yellow','Yellow'),('orange','Orange')],
          validators=[DataRequired(message='Color Field Empty')], default='blue')
  all_day = BooleanField('All Day?')
  submit = SubmitField('Submit')

  def validate(self):
    if self.date_start.data > self.date_end.data:
      raise ValidationError('Start Date Occurs Later Than End Date.')
    else:
      return True

class AppointmentFilterForm(FlaskForm):
  user = SelectField('Hospital Doctors: ')
  patient = SelectField('Patient: ')
  treatment = SelectField('Treatment: ')
  submit2 = SubmitField('Filter')

# SOME RULES
# HAS TO FILTER through either the current user OR their hospital OR users in their hospital

# select field choices
# patients (type in fullname)
# treatment (type in name)
# title (type in title)
# HOSPITAL DOES NOT HAVE TO BE ITS OWN FORM FIELD. IT CAN BE THE ALL OPTION!!!!!!!!!!
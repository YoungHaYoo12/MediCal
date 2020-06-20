from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField,TextAreaField,SelectField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired

class AppointmentForm(FlaskForm):
  title = StringField('Title',validators=[DataRequired(message='Title Field Empty')],default='')
  description = TextAreaField('Description',validators=[DataRequired(message='Description Field Empty')])
  date_start = DateTimeLocalField('Start Time (EDT)',validators=[DataRequired(message='Start Field Empty')],format='%Y-%m-%dT%H:%M',default=datetime.utcnow)
  date_end = DateTimeLocalField('End Time (EDT)',validators=[DataRequired(message='End Field Empty')],format='%Y-%m-%dT%H:%M',default=datetime.utcnow)
  treatment = SelectField('Treatment')
  patient = SelectField('Patient')
  submit = SubmitField('Submit')
from flask_wtf import FlaskForm
from wtforms import DateTimeField,StringField, SelectField, SubmitField,TextAreaField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateTimeLocalField

class TreatmentTableAddForm(FlaskForm):
  name = StringField('Table Name',validators=[DataRequired(message='Table Field Empty')])
  submit = SubmitField('Add Table')

class TreatmentTableEditForm(FlaskForm):
  name = StringField('Table Name',validators=[DataRequired(message='Table Field Empty')])
  submit = SubmitField('Update Table')

class TreatmentTableEntryAddForm(FlaskForm):
  treatment = SelectField('Treatment')
  date = DateTimeLocalField('Date',validators=[DataRequired(message='Date Field Empty')],format='%Y-%m-%dT%H:%M')

  amount = StringField('Amount')
  note = StringField('Additional Notes')
  submit = SubmitField('Add Entry')
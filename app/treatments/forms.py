from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TreatmentAddForm(FlaskForm):
  name = StringField('Treatment Name',validators=[DataRequired(message='Name Field Empty')])
  submit = SubmitField('Add Treatment')

class TreatmentEditForm(FlaskForm):
  name = StringField('Treatment Name',validators=[DataRequired(message='Name Field Empty')])
  submit = SubmitField('Edit Treatment')
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, DataRequired, Length

class TreatmentForm(FlaskForm):
  name = StringField('Treatment Name',validators=[DataRequired(message='Name Field Empty')])
  submit = SubmitField('Add Treatment')
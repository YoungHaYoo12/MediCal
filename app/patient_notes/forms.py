from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,SubmitField
from wtforms.validators import DataRequired

class PatientNoteAddForm(FlaskForm):
  title = StringField('Title', validators=[DataRequired(message='Title Field Empty')])
  notes = PageDownField('Notes',validators=[DataRequired(message='Notes Field Empty')])
  submit = SubmitField('Post')
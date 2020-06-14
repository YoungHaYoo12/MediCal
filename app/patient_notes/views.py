from flask import render_template
from app.patient_notes import patient_notes

@patient_notes.route('/')
def index():
  return "Patient Notes"
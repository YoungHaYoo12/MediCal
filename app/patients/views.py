from flask import render_template
from app.patients import patients

@patients.route('/')
def index():
  return "Patients"
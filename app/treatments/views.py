from flask import render_template
from app.treatments import treatments

@treatments.route('/')
def index():
  return "Treatments Page"
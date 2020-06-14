from flask import render_template
from app.appointments import appointments

@appointments.route('/')
def index():
  return "Appointments"
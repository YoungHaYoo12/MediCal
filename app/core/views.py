from flask import render_template
from app.core import core
from calendar import HTMLCalendar

@core.route('/')
def index():
  return render_template('index.html')

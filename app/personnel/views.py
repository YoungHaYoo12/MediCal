from flask import render_template
from app.personnel import personnel

@personnel.route('/')
def index():
  return "Personnel"
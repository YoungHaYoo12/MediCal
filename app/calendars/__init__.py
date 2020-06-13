from flask import Blueprint

calendars = Blueprint('calendars', __name__)

from app.calendars import views
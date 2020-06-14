from flask import Blueprint

appointments = Blueprint('appointments', __name__)

from app.appointments import views
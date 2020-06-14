from flask import Blueprint

patients = Blueprint('patients', __name__)

from app.patients import views
from flask import Blueprint

patient_notes = Blueprint('patient_notes', __name__)

from app.patient_notes import views
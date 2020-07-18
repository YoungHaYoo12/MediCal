from flask import Blueprint 

treatment_tables = Blueprint('treatment_tables',__name__)

from app.treatment_tables import views
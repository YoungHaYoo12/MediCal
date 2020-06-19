from flask import Blueprint

treatments = Blueprint('treatments', __name__)

from app.treatments import views
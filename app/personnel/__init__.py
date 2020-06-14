from flask import Blueprint

personnel = Blueprint('personnel', __name__)

from app.personnel import views
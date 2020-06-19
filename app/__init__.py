from config import config 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment

db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)

  # Initialize Flask Extension Instances 
  db.init_app(app)
  moment.init_app(app)
  login_manager.init_app(app)

  # Register blueprints
  from app.auth import auth as auth_blueprint
  from app.core import core as core_blueprint
  from app.calendars import calendars as calendars_blueprint
  from app.appointments import appointments as appointments_blueprint
  from app.patient_notes import patient_notes as patient_notes_blueprint
  from app.patients import patients as patients_blueprint
  from app.personnel import personnel as personnel_blueprint
  from app.treatments import treatments as treatments_blueprint

  app.register_blueprint(auth_blueprint,url_prefix='/auth')
  app.register_blueprint(core_blueprint)
  app.register_blueprint(calendars_blueprint,url_prefix='/calendars')
  app.register_blueprint(appointments_blueprint,url_prefix='/appointments')
  app.register_blueprint(patient_notes_blueprint,url_prefix='/patient_notes')
  app.register_blueprint(patients_blueprint,url_prefix='/patients')
  app.register_blueprint(personnel_blueprint,url_prefix='/personnel')
  app.register_blueprint(treatments_blueprint,url_prefix='/treatments')

  return app
from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

class Treatment(db.Model):
  __tablename__ = 'treatments'
  id = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.String(128),index=True,unique=True)
  appointments = db.relationship('Appointment',backref='treatment',lazy='dynamic')
  
  def __init__(self,name):
    self.name = name
  
  def __repr__(self):
    return f"{self.name}"
 
# Table storing for many to many relationship between Personnel and Patient models
relationships = db.Table('relationships',
               db.Column('patient_id',db.Integer,db.ForeignKey('patients.id')),
               db.Column('personnel_id',db.Integer,db.ForeignKey('personnel.id'))
               )
 
class Patient(db.Model):
  __tablename__ = 'patients'
  id = db.Column(db.Integer,primary_key=True)
  first_name = db.Column(db.String(64),index=True)
  last_name = db.Column(db.String(64),index=True)
  email = db.Column(db.String(64),index=True,unique=True)
  
  patient_notes = db.relationship('PatientNote',backref='patient',lazy='dynamic')
  appointments = db.relationship('Appointment',backref='patient',lazy='dynamic')
  personnel = db.relationship('Personnel',
                         secondary=relationships,
                         backref=db.backref('patients',lazy='dynamic'),
                         lazy='dynamic')
  
  def __init__(self,first_name,last_name,email):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
  
  def __repr__(self):
    return f"{self.first_name} {self.last_name}"
 
# Doctor's notes on patient
class PatientNote(db.Model):
  __tablename__ = 'patient_notes'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(64))
  notes = db.Column(db.Text)
  date_added = db.Column(db.DateTime,default=datetime.utcnow)
  date_modified = db.Column(db.DateTime,default=datetime.utcnow)
  
  patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
  personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'))
  
  def __init__(self,title,notes):
    self.title = title
    self.notes = notes
  
  def __repr__(self):
    return f"{self.title}"
 
# Appointment
class Appointment(db.Model):
  __tablename__ = 'appointments'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(64))
  description = db.Column(db.Text)
  date_start = db.Column(db.DateTime)
  date_end = db.Column(db.DateTime)
  
  treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'))
  patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
  personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'))
  
  def __init__(self,title,description,date_start,date_end):
    self.title = title
    self.description = description
    self.date_start = date_start
    self.date_end = date_end
  
  def __repr__(self):
    return f"{self.title}"

@login_manager.user_loader
def load_user(user_id):
  return Personnel.query.get(int(user_id))

# Medical Personnel (User of the web app)
class Personnel(db.Model):
  __tablename__ = 'personnel'
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(64),index=True)
  last_name = db.Column(db.String(64),index=True)
  email = db.Column(db.String(64),unique=True,index=True)
  password_hash = db.Column(db.String(128))
  
  patient_notes = db.relationship('PatientNote',backref='personnel',lazy='dynamic')
  appointments = db.relationship('Appointment',backref='personnel',lazy='dynamic')
  
  @property
  def password(self):
    raise AttributeError('password is not a readable attribute')
  
  @password.setter
  def password(self,password):
    self.password_hash = generate_password_hash(password)
  
  def verify_password(self,password):
    return check_password_hash(self.password_hash,password)
  
  def __init__(self,first_name,last_name,email,password):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password
  
  def __repr__(self):
    return f"<Personnel {self.email}>"
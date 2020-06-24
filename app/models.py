from app import db, login_manager
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask_login import UserMixin
from markdown import markdown
import bleach
from werkzeug.security import generate_password_hash,check_password_hash

# Table storing for many to many relationship between Personnel and Patient models
relationships = db.Table('relationships',
               db.Column('patient_id',db.Integer,db.ForeignKey('patients.id')),
               db.Column('user_id',db.Integer,db.ForeignKey('users.id'))
               )

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# Medical Personnel (User of the web app)
class User(db.Model,UserMixin):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(64),index=True)
  last_name = db.Column(db.String(64),index=True)
  username = db.Column(db.String(64),unique=True,index=True)
  email = db.Column(db.String(64),unique=True,index=True)
  password_hash = db.Column(db.String(128))
  
  hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
  patient_notes = db.relationship('PatientNote',backref='user',lazy='dynamic',cascade="all, delete-orphan")
  appointments = db.relationship('Appointment',backref='user',lazy='dynamic',cascade="all, delete-orphan")
  
  def __init__(self,first_name,last_name,username,email,password):
    self.first_name = first_name
    self.last_name = last_name
    self.username = username
    self.email = email
    self.password = password

  @property
  def password(self):
    raise AttributeError('password is not a readable attribute')
  
  @password.setter
  def password(self,password):
    self.password_hash = generate_password_hash(password)
  
  def verify_password(self,password):
    return check_password_hash(self.password_hash,password)

  def __repr__(self):
    return f"<User {self.email}>"

class Patient(db.Model):
  __tablename__ = 'patients'
  id = db.Column(db.Integer,primary_key=True)
  first_name = db.Column(db.String(64),index=True)
  last_name = db.Column(db.String(64),index=True)
  email = db.Column(db.String(64),index=True,unique=True)
  
  patient_notes = db.relationship('PatientNote',backref='patient',lazy='dynamic',cascade="all, delete-orphan")
  appointments = db.relationship('Appointment',backref='patient',lazy='dynamic',cascade="all, delete-orphan")
  users = db.relationship('User',
                         secondary=relationships,
                         backref=db.backref('patients',lazy='dynamic'),
                         lazy='dynamic')
  
  @property
  def fullname(self):
    return f"{self.first_name} {self.last_name}"

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
  notes_html = db.Column(db.Text)
  date_added = db.Column(db.DateTime,default=datetime.utcnow)
  date_modified = db.Column(db.DateTime,default=datetime.utcnow)
  
  patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  
  def refresh(self):
    self.date_modified = datetime.utcnow()
    db.session.commit()
  
  # static method for markdown to html conversion
  @staticmethod
  def on_changed_notes(target,value,oldvalue,initiator):
    allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul','h1', 'h2', 'h3', 'p']
    target.notes_html = bleach.linkify(bleach.clean(markdown(value,output_format='html'),tags=allowed_tags,strip=True))

  def __init__(self,title,notes):
    self.title = title
    self.notes = notes
  
  def __repr__(self):
    return f"{self.title}"
 
class Treatment(db.Model):
  __tablename__ = 'treatments'
  id = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.String(128),index=True)
  appointments = db.relationship('Appointment',backref='treatment',lazy='dynamic',cascade="all, delete-orphan")

  hospital_id = db.Column(db.Integer,db.ForeignKey('hospitals.id'))

  def __init__(self,name):
    self.name = name
  
  def __repr__(self):
    return f"{self.name}"
 
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
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  
  # Returns appointments within given year and month
  def get_appointments(year,month,day):
    query_start = datetime(year,month,day,0,0,0,0)
    query_end = query_start + relativedelta(days=1)
    return Appointment.query.filter(((Appointment.date_start <= query_start) & (Appointment.date_end >= query_end)) | ((Appointment.date_start >= query_start) & (Appointment.date_start < query_end)) | ((Appointment.date_end > query_start) & (Appointment.date_end < query_end)))
    # 1: appointment start is less than query date start AND appointment end is greater than query date end
    # 2: appointment start is greater than query date start and less than query date end 
    # 3: appointment end is greater than query date start and less than query date end

  # filter appointments on a particular date by user, patient, treatment, hospital, title (of appointment)
  def get_filtered_appointments(year,month,day,user=None,patient=None,treatment=None,hospital=None,title=None):
    query = Appointment.get_appointments(year,month,day)
    if hospital is not None:
      query = query.join(User, Appointment.user_id==User.id).join(Hospital,User.hospital_id==Hospital.id).filter(Hospital.id == hospital.id)
    if user is not None:
      query = query.filter(Appointment.user_id == user.id)
    if patient is not None:
      query = query.filter(Appointment.patient_id == patient.id)
    if treatment is not None:
      query = query.filter(Appointment.treatment_id == treatment.id)
    if title is not None:
      query = query.filter(Appointment.title == title)
    
    return query.order_by(Appointment.date_start.desc())

  def __init__(self,title,description,date_start,date_end):
    self.title = title
    self.description = description
    self.date_start = date_start
    self.date_end = date_end
  
  def __repr__(self):
    return f"{self.title}"

class Hospital(db.Model):
  __tablename__ = 'hospitals'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64),unique=True,index=True)

  users = db.relationship('User',backref='hospital',lazy='dynamic',cascade="all, delete-orphan")
  treatments = db.relationship('Treatment',backref='hospital',lazy='dynamic',cascade="all, delete-orphan")

  def get_patients(self):
    return Patient.query.join(relationships,relationships.columns.patient_id==Patient.id).join(User,relationships.columns.user_id==User.id).filter(User.hospital_id == self.id).order_by(Patient.last_name.asc())    

  def __init__(self,name):
    self.name = name
  
  def __repr__(self):
    return f"<Hospital {self.name}>"

# Listeners
db.event.listen(PatientNote.notes, 'set', PatientNote.on_changed_notes)
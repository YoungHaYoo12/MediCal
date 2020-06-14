from app import db
from datetime import datetime

class Treatment(db.Model):
  __tablename__ = 'treatments'
  id = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.String(128),index=True,unique=True)
  appointments = db.relationship('Appointment',backref='treatment',lazy='dynamic')

  def __repr__(self):
    return f"{self.name}"

# Table storing for many to many relationship between Staff and Patient models
relationships = db.Table('relationships',
                db.Column('patient_id',db.Integer,db.ForeignKey('patients.id')),
                db.Column('personnel_id',db.Integer,db.ForeignKey('personnel.id'))
                )

class Patient(db.Model):
  __tablename__ = 'patients'
  id = db.Column(db.Integer,primary_key=True)
  first_name = db.Column(db.String(64),index=True)
  last_name = db.Column(db.String(64,index=True))
  email = db.Column(db.String(64),index=True,unique=True)

  patient_notes = db.relationship('PatientNote',backref='patient',lazy='dynamic')
  appointments = db.relationship('Appointment',backref='patient',lazy='dynamic')
  personnel = db.relationship('Staff',
                          secondary=relationships,
                          backref=db.backref('patients',lazy='dynamic'),
                          lazy='dynamic')

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

  def __repr__(self):
    return f"{self.title}"

# Medical Personnel (User of the web app)
class Personnel(db.Model):
  __tablename__ = 'personnel'
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(64),index=True)
  last_name = db.Column(db.String(64),index=True)
  email = db.Column(db.String(64),unique=True,index=True)

  patient_notes = db.relationship('PatientNote',backref='personnel',lazy='dynamic')
  appointments = db.relationship('Appointment',backref='personnel',lazy='dynamic')

  def __repr__(self):
    return f"<Personnel {self.email}>"
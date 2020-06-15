import unittest
from sqlalchemy.exc import IntegrityError
from app import create_app, db
from app.models import Appointment, Patient, User, Treatment, PatientNote
from datetime import datetime,timedelta

class FlaskTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

class TreatmentModelTestCase(FlaskTestCase):
  def test_id(self):
    treatment = Treatment(name='medicine')
    db.session.add(treatment)
    db.session.commit()
    self.assertEqual(treatment.id, 1)

  def test_repr(self):
    treatment = Treatment(name='therapy')
    self.assertEqual(treatment.__repr__(), 'therapy')

  def test_name_assignment(self):
    treatment = Treatment(name='medicine')
    self.assertEqual(treatment.name,'medicine')
  
  def test_name_is_unique(self):
    treatment1 = Treatment(name='flu vaccine')
    treatment2 = Treatment(name='flu vaccine')
    
    db.session.add(treatment1)
    db.session.commit()

    with self.assertRaises(IntegrityError):
      db.session.add(treatment2)
      db.session.commit()

class PatientModelTestCase(FlaskTestCase):
  def test_id(self):
    patient = Patient(first_name='John',last_name='Doe',email='johndoe@example.com')
    db.session.add(patient)
    db.session.commit()
    self.assertEqual(patient.id, 1)

  def test_repr(self):
    patient = Patient(first_name='John',last_name='Doe',email='johndoe@example.com')
    self.assertEqual(patient.__repr__(), 'John Doe')

  def test_name_assignment(self):
    patient = Patient(first_name='John',last_name='Doe',email='johndoe@example.com')
    self.assertEqual(patient.first_name,'John')
    self.assertEqual(patient.last_name,'Doe')

  def test_email_assignment(self):
    patient = Patient(first_name='John',last_name='Doe',email='johndoe@example.com')
    self.assertEqual(patient.email,'johndoe@example.com')

  def test_email_is_unique(self):
    patient1 = Patient(first_name='John',last_name='Doe',email='example@example.com')
    patient2 = Patient(first_name='Jane',last_name='Doe',email='example@example.com')
    
    db.session.add(patient1)
    db.session.commit()

    with self.assertRaises(IntegrityError):
      db.session.add(patient2)
      db.session.commit()

class PatientNoteModelTestCase(FlaskTestCase):
  def test_id(self):
    note = PatientNote(title='title',notes='notes')
    db.session.add(note)
    db.session.commit()
    self.assertEqual(note.id, 1)
    
  def test_repr(self):
    note = PatientNote(title='title',notes='notes')
    self.assertEqual(note.__repr__(), 'title')

  def test_title_and_notes_assignment(self):
    note = PatientNote(title='title',notes='notes')
    self.assertEqual(note.title, 'title')
    self.assertEqual(note.notes, 'notes')
  
  def test_dates_assignment(self):
    before = datetime.utcnow()
    note = PatientNote(title='title',notes='notes')
    db.session.add(note)
    db.session.commit()
    after = datetime.utcnow()
    self.assertTrue(note.date_added > before and note.date_added < after)
    self.assertTrue(note.date_modified > before and note.date_modified < after)

class AppointmentModelTestCase(FlaskTestCase):
  def test_id(self):
    start = datetime.utcnow()
    end = datetime.utcnow() + timedelta(days=1)
    appointment = Appointment(title='title',description='description',
                  date_start=start, date_end = end)
    db.session.add(appointment)
    db.session.commit()
    self.assertEqual(appointment.id, 1)
    
  def test_repr(self):
    start = datetime.utcnow()
    end = datetime.utcnow() + timedelta(days=1)
    appointment = Appointment(title='title',description='description',
                  date_start=start, date_end = end)
    self.assertEqual(appointment.__repr__(), 'title')

  def test_attributes_assignment(self):
    start = datetime.utcnow()
    end = datetime.utcnow() + timedelta(days=1)
    appointment = Appointment(title='title',description='description',
                  date_start=start, date_end = end)
    self.assertEqual(appointment.title, 'title')
    self.assertEqual(appointment.description, 'description')
    self.assertEqual(appointment.date_start, start)
    self.assertEqual(appointment.date_end, end)

class UserModelTestCase(FlaskTestCase):
  def test_id(self):
    user = User(first_name='one',last_name='two',email='one@two.com',username='username',password='one')
    db.session.add(user)
    db.session.commit()
    self.assertEqual(user.id,1)
  
  def test_attributes_assignment(self):
    user = User(first_name='one',last_name='two',username='username',email='one@two.com',password='one')
    self.assertEqual(user.first_name,'one')
    self.assertEqual(user.last_name,'two')
    self.assertEqual(user.email,'one@two.com')

  def test_email_is_unique(self):
    user1 = User(first_name='John',last_name='Doe',username='username',email='example@example.com',password='one')
    user2 = User(first_name='Jane',last_name='Doe',username='username',email='example@example.com',password='one')
    
    db.session.add(user1)
    db.session.commit()

    with self.assertRaises(IntegrityError):
      db.session.add(user2)
      db.session.commit()

  def test_repr(self):
    user1 = User(first_name='John',last_name='Doe',username='username',email='example@example.com',password='one')
    self.assertEqual(user1.__repr__(),'<User example@example.com>')

  def test_password_setter(self):
    u = User(first_name='John',last_name='Doe',username='username',email='example@example.com',password='one')
    self.assertTrue(u.password_hash is not None)
  
  def test_no_password_getter(self):
    u = User(first_name='John',last_name='Doe',username='username',email='example@example.com',password='one')
    with self.assertRaises(AttributeError):
      u.password
  
  def test_password_verification(self):
    u = User(first_name='John',last_name='Doe',username='username',email='example@example.com',password='one')
    self.assertTrue(u.verify_password('one'))
    self.assertFalse(u.verify_password('two'))

  def test_password_salts_are_random(self):
    u1 = User(first_name='John',last_name='Doe',username='username',email='example@example.com',password='one')
    u2 = User(first_name='John',last_name='Doe',username='username',email='example@example.com',password='one')
    self.assertTrue(u1.password_hash != u2.password_hash)

class ModelRelationshipsTestCase(FlaskTestCase):
  def test_patient_notes_relationship(self):
    patient = Patient(first_name='John',last_name='Elliot',email="john@elliot.com")
    user = User(first_name='John',last_name='Elliot',username='username',email="john@elliot.com",password='one')  
    patient_note1 = PatientNote(title='title1',notes='note1')
    patient_note2 = PatientNote(title='title2',notes='note2')

    # before connecting
    self.assertEqual(len(patient.patient_notes.all()), 0)
    self.assertEqual(len(user.patient_notes.all()), 0)

    # after connecting patient_note1
    patient_note1.patient = patient
    patient_note1.user = user

    db.session.add_all([patient,user,patient_note1,patient_note2])
    db.session.commit()
    self.assertEqual(len(patient.patient_notes.all()), 1)
    self.assertTrue(patient_note1 in patient.patient_notes.all())
    self.assertEqual(patient_note1.patient_id, patient.id)
    self.assertFalse(patient_note2 in patient.patient_notes.all())
    self.assertNotEqual(patient_note2.patient_id, patient.id)
    self.assertEqual(len(user.patient_notes.all()), 1)
    self.assertTrue(patient_note1 in user.patient_notes.all())
    self.assertEqual(patient_note1.user_id, user.id)
    self.assertFalse(patient_note2 in user.patient_notes.all())
    self.assertNotEqual(patient_note2.user_id, user.id)

  def test_appointments_relationship(self):
    start = datetime.utcnow()
    end = datetime.utcnow() + timedelta(days=1)
    appointment1 = Appointment(title='title1',description='description1',
                  date_start=start, date_end = end)
    appointment2 = Appointment(title='title2',description='description2',
                  date_start=start, date_end = end)
    patient = Patient(first_name='John',last_name='Elliot',email="john@elliot.com")
    user = User(first_name='John',last_name='Elliot',username='username',email="john@elliot.com",password='one')  
    treatment = Treatment(name='Tylenol')

    # before connecting
    self.assertEqual(len(patient.appointments.all()), 0)
    self.assertEqual(len(user.appointments.all()), 0)
    self.assertEqual(len(treatment.appointments.all()), 0)

    # after connecting appointment1
    appointment1.patient = patient
    appointment1.user = user
    appointment1.treatment = treatment

    db.session.add_all([patient,user,treatment,appointment1,appointment2])
    db.session.commit()

    self.assertEqual(len(patient.appointments.all()), 1)
    self.assertTrue(appointment1 in patient.appointments.all())
    self.assertEqual(appointment1.patient_id, patient.id)
    self.assertFalse(appointment2 in patient.appointments.all())
    self.assertNotEqual(appointment2.patient_id, patient.id)    

    self.assertEqual(len(user.appointments.all()), 1)
    self.assertTrue(appointment1 in user.appointments.all())
    self.assertEqual(appointment1.user_id, user.id)
    self.assertFalse(appointment2 in user.appointments.all())
    self.assertNotEqual(appointment2.user_id, user.id)    

    self.assertEqual(len(treatment.appointments.all()), 1)
    self.assertTrue(appointment1 in treatment.appointments.all())
    self.assertEqual(appointment1.treatment_id, treatment.id)
    self.assertFalse(appointment2 in treatment.appointments.all())
    self.assertNotEqual(appointment2.treatment_id, treatment.id)    

  def test_user_patient_relationship(self):
    patient1 = Patient(first_name='one',last_name='one',email='one')
    patient2 = Patient(first_name='two',last_name='two',email='two')
    user1 = User(first_name='three',last_name='three',username='username',email='three',password='one')
    user2 = User(first_name='four',last_name='four',username='username',email='four',password='one')

    # before connecting
    self.assertEqual(len(patient1.users.all()),0)
    self.assertEqual(len(patient2.users.all()),0)
    self.assertEqual(len(user1.patients.all()),0)
    self.assertEqual(len(user2.patients.all()),0)

    # connect patients to user1
    user1.patients.append(patient1)
    user1.patients.append(patient2)
    self.assertEqual(len(user1.patients.all()),2)
    self.assertTrue(patient1 in user1.patients.all())
    self.assertTrue(patient2 in user1.patients.all())
    self.assertFalse(patient1 in user2.patients.all())
    self.assertFalse(patient2 in user2.patients.all())
    self.assertTrue(user1 in patient1.users.all())
    self.assertTrue(user1 in patient2.users.all())
    self.assertFalse(user2 in patient1.users.all())
    self.assertFalse(user2 in patient2.users.all())

    #undo
    user1.patients.remove(patient1)
    user1.patients.remove(patient2)

    # connect users to patient1
    patient1.users.append(user1)
    patient1.users.append(user2)
    self.assertEqual(len(patient1.users.all()),2)
    self.assertTrue(user1 in patient1.users.all())
    self.assertTrue(user2 in patient1.users.all())
    self.assertFalse(user1 in patient2.users.all())
    self.assertFalse(user2 in patient2.users.all())
    self.assertTrue(patient1 in user1.patients.all())
    self.assertTrue(patient1 in user2.patients.all())
    self.assertFalse(patient2 in user1.patients.all())
    self.assertFalse(patient2 in user2.patients.all())
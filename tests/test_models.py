import unittest
from sqlalchemy.exc import IntegrityError
from app import create_app, db
from app.models import Appointment, Patient, Personnel, Treatment, PatientNote
from datetime import datetime

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
import unittest
from flask import url_for
from flask_login import current_user
from app import db, create_app
from app.models import User, Patient, PatientNote
from datetime import datetime

class PatientNotesTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client(use_cookies=True)

    # model instances used in unit tests
    user1 = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    user2 = User(first_name='two',last_name='two',username='two',email='two@two.com',password='two')    
    patient1 = Patient(first_name='patient1',last_name='patient1',email='patient1@gmail.com')
    patient2 = Patient(first_name='patient2',last_name='patient2',email='patient2@gmail.com')
    patient_note_1 = PatientNote(title='title1',notes='notes1')
    patient_note_2 = PatientNote(title='title2',notes='notes2')
    patient_note_1.user = user1
    patient_note_2.user = user2
    patient_note_1.patient = patient1
    patient_note_2.patient = patient2
    patient1.users.append(user1)
    patient2.users.append(user2)    
    db.session.add_all([user1,user2,patient1,patient2,patient_note_1,patient_note_2])
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_invalid_user(self):
    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'username':'one',
        'password': 'one' 
      }
      )

      response = self.client.get(url_for('patient_notes.list',patient_id=100))
      self.assertEqual(response.status_code,404)

      response = self.client.get(url_for('patient_notes.add',patient_id=100))
      self.assertEqual(response.status_code,404)

      response = self.client.get(url_for('patient_notes.patient_note',patient_note_id=100))
      self.assertEqual(response.status_code,404)

      response = self.client.get(url_for('patient_notes.edit',patient_note_id=100))
      self.assertEqual(response.status_code,404)

      response = self.client.get(url_for('patient_notes.delete',patient_note_id=100))
      self.assertEqual(response.status_code,404)

  def test_validate_user(self):
    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'username':'one',
        'password': 'one' 
      }
      )
      response = self.client.get(url_for('patient_notes.list',patient_id=2))
      self.assertEqual(response.status_code,403)

      response = self.client.get(url_for('patient_notes.add',patient_id=2))
      self.assertEqual(response.status_code,403)

      response = self.client.get(url_for('patient_notes.patient_note',patient_note_id=2))
      self.assertEqual(response.status_code,403)

      response = self.client.get(url_for('patient_notes.edit',patient_note_id=2))
      self.assertEqual(response.status_code,403)

      response = self.client.get(url_for('patient_notes.delete',patient_note_id=2))
      self.assertEqual(response.status_code,403)
  
  def test_patient_notes_list(self):
    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'username':'one',
        'password': 'one' 
      }
      )

      response = self.client.get(url_for('patient_notes.list',patient_id=1))
      data = response.get_data(as_text=True)
      self.assertEqual(response.status_code,200)
      self.assertTrue('Patient Notes for patient1' in data)
      self.assertTrue('one' in data)
      self.assertTrue('title1' in data)
      self.assertTrue('notes1' in data)
  
  def test_patient_notes_patient_note(self):
    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'username':'one',
        'password': 'one' 
      }
      )

      response = self.client.get(url_for('patient_notes.patient_note',patient_note_id=1))
      data = response.get_data(as_text=True)
      self.assertEqual(response.status_code,200)
      self.assertTrue('patient1' in data)
      self.assertTrue('one' in data)
      self.assertTrue('title1' in data)
      self.assertTrue('notes1' in data)  
  
  def test_patient_notes_add(self):
    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'username':'one',
        'password': 'one' 
      }
      )

      # GET
      response = self.client.get(url_for('patient_notes.add',patient_id=1))
      data = response.get_data(as_text=True)
      self.assertEqual(response.status_code,200)
      self.assertTrue('patient1' in data)

      # POST
      response = self.client.post(url_for('patient_notes.add',patient_id=1),data = {
        'title':'posted title',
        'notes':'posted notes'
      }, follow_redirects=True)
      data = response.get_data(as_text=True)
      self.assertEqual(response.status_code,200)
      self.assertTrue('posted title' in data)
      self.assertTrue('posted notes' in data)
      self.assertTrue('Patient Note Successfully Posted.' in data)
      posted_note = PatientNote.query.get(3)
      patient = Patient.query.get(1)
      self.assertTrue(posted_note.user == current_user)
      self.assertTrue(posted_note.patient == patient)
  
  def test_patient_notes_edit(self):
    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'username':'one',
        'password': 'one' 
      }
      )

      # GET
      response = self.client.get(url_for('patient_notes.edit',patient_note_id=1))
      patient_note = PatientNote.query.get(1)
      data = response.get_data(as_text=True)
      self.assertEqual(response.status_code,200)
      self.assertTrue(patient_note.title in data)
      self.assertTrue(patient_note.notes in data)

      # POST
      time_before = datetime.utcnow()
      response = self.client.post(url_for('patient_notes.edit',patient_note_id=1),data={
        'title':'edited title',
        'notes':'edited notes'
      },follow_redirects=True)
      time_after = datetime.utcnow()
      data = response.get_data(as_text=True)
      self.assertEqual(response.status_code,200)
      self.assertTrue('edited title' in data)
      self.assertTrue('edited notes' in data)
      self.assertTrue('Patient Note Successfully Edited' in data)

      patient_note = PatientNote.query.get(1)
      self.assertEqual(patient_note.title,'edited title')
      self.assertEqual(patient_note.notes,'edited notes')
      self.assertTrue(patient_note.date_modified > time_before)
      self.assertTrue(patient_note.date_modified < time_after)
  
  def test_patient_notes_delete(self):
    # before deletion
    self.assertEqual(len(PatientNote.query.all()),2)

    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'username':'one',
        'password': 'one' 
      }
      )

      response = self.client.get(url_for('patient_notes.delete',patient_note_id=1),follow_redirects=True)
      data = response.get_data(as_text=True)

      # after deletion
      self.assertTrue('Patient Note Successfully Deleted' in data)
      self.assertEqual(len(PatientNote.query.all()),1)
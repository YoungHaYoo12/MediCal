import unittest
from flask import url_for
from flask_login import current_user
from app import db
from app.models import User, Patient, Hospital
from base_case import FlaskClientTestCase

class PatientTestCase(FlaskClientTestCase):
  def test_patients_edit(self):
    user1 = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    user2 = User(first_name='two',last_name='two',username='two',email='two@two.com',password='two')    
    patient1 = Patient(first_name='patient1',last_name='patient1',email='patient1@gmail.com')
    patient2 = Patient(first_name='patient2',last_name='patient2',email='patient2@gmail.com')
    patient1.users.append(user1)
    patient2.users.append(user2)    
    db.session.add_all([user1,user2,patient1,patient2])
    db.session.commit()

    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'username':'one',
        'password': 'one' 
      }
      )

      # patient that does not exist
      response = self.client.get(url_for('patients.edit',id=100))
      self.assertEqual(response.status_code,404)

      # patient that does not belong to current user
      response = self.client.get(url_for('patients.edit',id=2))
      self.assertEqual(response.status_code,403)

      # patient that does belong to current user (GET)
      response = self.client.get(url_for('patients.edit',id=1))
      data = response.get_data(as_text=True)
      self.assertTrue('patient1' in data)
      self.assertTrue('patient1@gmail.com' in data)

      # patient that does belong to current user (POST)
      response = self.client.post(url_for('patients.edit',id=1),data={
        'first_name':'new first_name',
        'last_name':'new last_name',
        'email':'new email'
      },follow_redirects=True)
      data = response.get_data(as_text=True)
      self.assertEqual(response.status_code,200)
      self.assertTrue('new first_name' in data)
      self.assertTrue('new last_name' in data)
      self.assertTrue('new email' in data)

  def test_patients_delete(self):
    user1 = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    user2 = User(first_name='two',last_name='two',username='two',email='two@two.com',password='two')    
    patient1 = Patient(first_name='patient1',last_name='patient1',email='patient1@gmail.com')
    patient2 = Patient(first_name='patient2',last_name='patient2',email='patient2@gmail.com')
    patient1.users.append(user1)
    patient2.users.append(user2)    
    db.session.add_all([user1,user2,patient1,patient2])
    db.session.commit()

    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'username':'one',
        'password': 'one' 
      }
      )

      # patient that does not exist
      response = self.client.get(url_for('patients.delete',id=100))
      self.assertEqual(response.status_code,404)

      # patient that does not belong to current user
      response = self.client.get(url_for('patients.delete',id=2))
      self.assertEqual(response.status_code,403)

      # patient that does belong to current user
      patient1 = Patient.query.get(1)
      self.assertEqual(len(current_user.patients.all()),1)
      self.assertTrue(patient1 in current_user.patients.all())
      response = self.client.get(url_for('patients.delete',id=1),follow_redirects=True)
      data = response.get_data(as_text=True)
      self.assertEqual(response.status_code,200)
      self.assertTrue('Patient Successfully Deleted' in data)
      self.assertEqual(len(current_user.patients.all()),0)
      self.assertFalse(patient1 in current_user.patients.all())

  def test_patients_patient(self):
    user1 = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    user2 = User(first_name='two',last_name='two',username='two',email='two@two.com',password='two')    
    patient1 = Patient(first_name='patient1',last_name='patient1',email='patient1@gmail.com')
    patient2 = Patient(first_name='patient2',last_name='patient2',email='patient2@gmail.com')
    patient1.users.append(user1)
    patient2.users.append(user2)    
    db.session.add_all([user1,user2,patient1,patient2])
    db.session.commit()

    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'username':'one',
        'password': 'one' 
      }
      )
      # test patient_id that does not exist
      response = self.client.get(url_for('patients.patient',id=100))
      self.assertEqual(response.status_code,404)

      # test patient that does not belong to current_user
      response = self.client.get(url_for('patients.patient',id=2))
      self.assertEqual(response.status_code,403)

      # test on patient that does belong to current user
      response = self.client.get(url_for('patients.patient',id=1))
      data = response.get_data(as_text=True)
      self.assertEqual(response.status_code,200)
      self.assertTrue('one' in data)
      self.assertTrue('patient1@gmail.com' in data)



  def test_patients_list(self):
    hospital1 = Hospital('Hospital1')
    hospital2 = Hospital('Hospital2')

    user1 = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    user2 = User(first_name='two',last_name='two',username='two',email='two@two.com',password='two')
    user3 = User(first_name='three',last_name='three',username='three',email='three@three.com',password='three')

    patient1 = Patient(first_name='patient1',last_name='patient1',email='patient1@gmail.com')
    patient2 = Patient(first_name='patient2',last_name='patient2',email='patient2@gmail.com')
    patient3 = Patient(first_name='patient3',last_name='patient3',email='patient3@gmail.com')

    user1.hospital = hospital1
    user2.hospital = hospital1
    user3.hospital = hospital2

    patient1.users.append(user1)
    patient2.users.append(user2)
    patient3.users.append(user3)

    db.session.add_all([user1,user2,user3,patient1,patient2,patient3,hospital1,hospital2])
    db.session.commit()

    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'username':'one',
        'password': 'one' 
      }
      )

      # when category='user'
      response = self.client.get(url_for('patients.list',category='user'))
      data = response.get_data(as_text = True)
      self.assertTrue('patient1' in data)
      self.assertFalse('patient2' in data)
      self.assertFalse('patient3' in data)

      # when category='hospital'
      response = self.client.get(url_for('patients.list',category='hospital'))
      data = response.get_data(as_text = True)
      self.assertTrue('patient1' in data)
      self.assertTrue('patient2' in data)
      self.assertFalse('patient3' in data)

      # when category equals neither
      response = self.client.get(url_for('patients.list',category='random'))
      self.assertEqual(response.status_code,404)

      # form testing
      response = self.client.post(url_for('patients.list',category='user'),data={
        'first_name': 'patient4',
        'last_name': 'patient4',
        'email':'patient4@gmail.com'
      },follow_redirects=True)
      self.assertEqual(response.status_code,200)
      data = response.get_data(as_text=True)
      patient_added = Patient.query.filter_by(email="patient4@gmail.com").first()
      self.assertTrue(patient_added in current_user.patients.all())

      self.assertTrue('New Patient Added' in data)
      self.assertTrue('patient4' in data)
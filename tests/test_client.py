import unittest
from datetime import datetime
from flask import url_for
from flask_login import current_user
from app import create_app, db
from app.models import User, Patient, PatientNote, Hospital

class FlaskClientTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client(use_cookies=True)
  
  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

class CoreTestCase(FlaskClientTestCase):
  def test_index(self):
    # test without login
    response = self.client.get(url_for('core.index'))
    data = response.get_data(as_text=True)

    self.assertEqual(response.status_code,200)
    self.assertTrue('Welcome to MediCal.' in data)
    self.assertTrue('GET STARTED' in data)

    # test with login
    user = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    db.session.add(user)
    db.session.commit()

    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'username':'one',
        'password': 'one' 
      }
      )
    
      response = self.client.get(url_for('core.index'))
      data = response.get_data(as_text=True)

      self.assertEqual(response.status_code,200)
      self.assertTrue('Welcome,' in data)
      self.assertTrue('one' in data)
      self.assertFalse('Get Started' in data)

class PatientTestCase(FlaskClientTestCase):
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
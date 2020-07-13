from flask import url_for
from app import db
from app.models import User, Hospital, Appointment,Patient
from base_case import FlaskClientTestCase
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
  
  def test_search_users(self):
    hospital = Hospital(name='hospital1')
    user = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    user2 = User(first_name='two',last_name='two',username='two',email='two@two.com',password='two')
    user.hospital = hospital
    user2.hospital = hospital
    db.session.add_all([user,user2,hospital])
    db.session.commit()

    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'username':'one',
        'password': 'one' 
      }
      )
        
      # without any session data stored 
      response = self.client.get(url_for('core.search_users'))
      data = response.get_data(as_text=True)
      # should return all users connected to hospital
      self.assertTrue('one' in data)
      self.assertTrue('two' in data)

      # filter search by username
      response = self.client.post(url_for('core.search_users'),data= {
        'username':'one',
      },follow_redirects=True)
      self.assertEqual(response.status_code,200)
      data = response.get_data(as_text=True)
      self.assertTrue('one' in data)
      self.assertFalse('two' in data)

      # filter search by first_name
      response = self.client.post(url_for('core.search_users'),data= {
        'first_name':'one',
      },follow_redirects=True)
      self.assertEqual(response.status_code,200)
      data = response.get_data(as_text=True)
      self.assertTrue('one' in data)
      self.assertFalse('two' in data)

      # filter search by last_name
      response = self.client.post(url_for('core.search_users'),data= {
        'last_name':'one'
      },follow_redirects=True)
      self.assertEqual(response.status_code,200)
      data = response.get_data(as_text=True)
      self.assertTrue('one' in data)
      self.assertFalse('two' in data)
  
  def test_user(self):
    hospital = Hospital(name='hospital1')
    hospital2 = Hospital(name='hospital2')
    user = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    user2 = User(first_name='two',last_name='two',username='two',email='two@two.com',password='two')
    user.hospital = hospital
    user2.hospital = hospital2

    patient1 = Patient(first_name='patient1',last_name='patient1',email='patient1@gmail.com')
    patient1.users.append(user)
    patient2 = Patient(first_name='patient2',last_name='patient2',email='patient2@gmail.com')

    db.session.add_all([user,user2,hospital,hospital2,patient1,patient2])
    db.session.commit()

    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'username':'one',
        'password': 'one' 
      }
      )

      # nonexistent user 
      response = self.client.get(url_for('core.user',username='notauser'))
      self.assertTrue(response.status_code,404)

      # invalid user (user not in same hospital)
      response = self.client.get(url_for('core.user',username='two'))
      self.assertTrue(response.status_code,403)

      response = self.client.get(url_for('core.user',username='one'))
      data = response.get_data(as_text=True)
      # test that patient1 in user page
      self.assertTrue('patient1' in data)
      self.assertFalse('patient2' in data)
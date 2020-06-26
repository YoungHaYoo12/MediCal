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

    today = datetime.utcnow()
    appointment1_time = today 
    appointment2_time = today + relativedelta(days=6)
    appointment3_time = today + relativedelta(days=29)
    appointment4_time = today - relativedelta(days=1)
    appointment5_time = today + relativedelta(days=100)

    appointment1 = Appointment(title='appointment1',description='asdf',date_start=appointment1_time,date_end=appointment1_time)
    appointment2 = Appointment(title='appointment2',description='asdf',date_start=appointment2_time,date_end=appointment2_time)
    appointment3 = Appointment(title='appointment3',description='asdf',date_start=appointment3_time,date_end=appointment3_time)
    appointment4 = Appointment(title='appointment4',description='asdf',date_start=appointment4_time,date_end=appointment4_time)
    appointment5 = Appointment(title='appointment5',description='asdf',date_start=appointment5_time,date_end=appointment5_time)

    appointment1.user = user
    appointment2.user = user
    appointment3.user = user
    appointment4.user = user
    appointment5.user = user

    db.session.add_all([user,user2,hospital,hospital2,appointment1,appointment2,appointment3,appointment4,appointment5,patient1,patient2])
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

      # test that appointments 1,2,3 are in data but not appointment 4 (which is before today) and 5 (which is more than 30 days later than today)
      response = self.client.get(url_for('core.user',username='one'))
      data = response.get_data(as_text=True)
      self.assertTrue('appointment1' in data)
      self.assertTrue('appointment2' in data)
      self.assertTrue('appointment3' in data)
      self.assertFalse('appointment4' in data)
      self.assertFalse('appointment5' in data)

      # test that patient1 in user page
      self.assertTrue('patient1' in data)
      self.assertFalse('patient2' in data)
from flask import url_for
from flask_login import current_user
from app.models import User, Hospital,Treatment
from base_case import FlaskClientTestCase
from app import db

class TreatmentsTestCase(FlaskClientTestCase):
  def test_treatments_list(self):
    # create model instances
    hospital1 = Hospital(name='hospital1')
    hospital2 = Hospital(name='hospital2')

    user1 = User(first_name='one',
    last_name='one',
    username='one',
    email='one@one.com',
    password='one')
    user2 = User(first_name='two',
    last_name='two',
    username='two',
    email='two@two.com',
    password='two')

    treatment1 = Treatment(name='treatment1')
    treatment2 = Treatment(name='treatment2')

    hospital1.treatments.append(treatment1)
    hospital1.treatments.append(treatment2)

    user1.hospital = hospital1
    user2.hospital = hospital2

    db.session.add_all([hospital1,hospital2,user1,user2,treatment1,treatment2])
    db.session.commit()

    # test for user1
    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'password': 'one' 
      }
      )
      response = self.client.get(url_for('treatments.list'))
      data = response.get_data(as_text=True)
      self.assertTrue('treatment1' in data)
      self.assertTrue('treatment2' in data)

    
    # test for user2
    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'two@two.com', 
        'password': 'two' 
      }
      )
      response = self.client.get(url_for('treatments.list'))
      data = response.get_data(as_text=True)
      self.assertFalse('treatment1' in data)
      self.assertFalse('treatment2' in data)

  def test_treatments_add(self):
    hospital1 = Hospital(name='hospital1')

    user = User(first_name='one',
    last_name='one',
    username='one',
    email='one@one.com',
    password='one')
    user.hospital = hospital1

    db.session.add_all([user,hospital1])
    db.session.commit()

    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'password': 'one' 
      }
      )
      # Invalid Submission
      response = self.client.post(url_for('treatments.add'),data={
        'name':""
      })
      self.assertNotEqual(response.status_code,302)

      # Treatment That Does Not Already Exist
      self.assertEqual(len(current_user.hospital.treatments.all()),0)
      response = self.client.post(url_for('treatments.add'),data={
        'name':'added_treatment'
      },follow_redirects=True)
      data = response.get_data(as_text=True)
      self.assertTrue('Treatment Successfully Added' in data)
      self.assertTrue('added_treatment' in data)
      self.assertEqual(len(current_user.hospital.treatments.all()),1)

  def test_treatments_delete(self):
    hospital1 = Hospital(name='hospital1')

    user = User(first_name='one',
    last_name='one',
    username='one',
    email='one@one.com',
    password='one')
    user.hospital = hospital1
    treatment = Treatment(name='treatment')
    treatment.hospital=hospital1

    treatment2 = Treatment(name='not part of hospital1')

    db.session.add_all([user,hospital1,treatment,treatment2])
    db.session.commit()

    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'password': 'one' 
      }
      )

      # treatment id does not exist
      response = self.client.get(url_for('treatments.delete',id=100))
      self.assertEqual(response.status_code,404)

      # user not validated 
      response = self.client.get(url_for('treatments.delete',id=2))
      self.assertEqual(response.status_code,403)

      # successful deletion
      self.assertEqual(len(current_user.hospital.treatments.all()),1)
      response = self.client.get(url_for('treatments.delete',id=1),follow_redirects=True)
      data = response.get_data(as_text=True)
      self.assertEqual(response.status_code,200)
      self.assertTrue('Treatment Successfully Deleted' in data)
      self.assertEqual(len(current_user.hospital.treatments.all()),0)
  
  def test_treatments_edit(self):
    hospital1 = Hospital(name='hospital1')

    user = User(first_name='one',
    last_name='one',
    username='one',
    email='one@one.com',
    password='one')
    user.hospital = hospital1
    treatment = Treatment(name='treatment')
    treatment.hospital=hospital1

    treatment2 = Treatment(name='not part of hospital1')

    db.session.add_all([user,hospital1,treatment,treatment2])
    db.session.commit()

    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'one@one.com', 
        'password': 'one' 
      }
      )

      # treatment id does not exist
      response = self.client.get(url_for('treatments.edit',id=100))
      self.assertEqual(response.status_code,404)

      # user not validated 
      response = self.client.get(url_for('treatments.edit',id=2))
      self.assertEqual(response.status_code,403)

      # successful edit
      response = self.client.post(url_for('treatments.edit',id=1),data={
        'name':'treatment edited'
      },follow_redirects=True)
      data = response.get_data(as_text=True)
      self.assertTrue('Treatment Successfully Edited' in data)
      treatment = current_user.hospital.treatments.all()[0]
      self.assertEqual(treatment.name,'treatment edited')
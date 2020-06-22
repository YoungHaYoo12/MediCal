from flask import url_for
from app import db
from app.models import User
from base_case import FlaskClientTestCase

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

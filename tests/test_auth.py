from flask import url_for
from app.models import User, Hospital
from base_case import FlaskClientTestCase
from app import create_app, db
from dateutil.relativedelta import relativedelta
from datetime import datetime

class AuthTestCase(FlaskClientTestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client(use_cookies=True)
    hospital = Hospital(name='Hospital1')
    db.session.add(hospital)
    db.session.commit()

    @self.app.context_processor
    def utility_processor():
        def get_curr_date():
            return datetime.utcnow()
        def get_next_month(year,month):
          curr = datetime(year=year,month=month,day=1)
          next_month = curr + relativedelta(months=1)
          return next_month
        def get_prev_month(year,month):
          curr = datetime(year=year,month=month,day=1)
          prev_month = curr - relativedelta(months=1)
          return prev_month
        return dict(get_curr_date=get_curr_date,
                    get_next_month=get_next_month,
                    get_prev_month=get_prev_month
                    )    
  
  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_auth_register(self):
    # register with empty data
    response = self.client.post(url_for('auth.register'), data= {
      'email':"",
      'username':"",
      'password':"",
      'password2':"",
      'first_name':"",
      'last_name':"",
      'hospital':""
    })
    self.assertNotEqual(response.status_code, 302)

    # register with invalid email
    response = self.client.post(url_for('auth.register'), data= {
      'email':"notanemail",
      'username':"two",
      'password':"two",
      'password2':"two",
      'first_name':"two",
      'last_name':"two",
      'hospital':"1"
    })
    self.assertNotEqual(response.status_code, 302)

    # register with invalid username
    response = self.client.post(url_for('auth.register'), data= {
      'email':"notanemail",
      'username':"",
      'password':"two",
      'password2':"two",
      'first_name':"two",
      'last_name':"two",
      'hospital':"1"
    })
    self.assertNotEqual(response.status_code, 302)    

    # register with unmatching passwords
    response = self.client.post(url_for('auth.register'), data= {
      'email':"notanemail",
      'username':"",
      'password':"two",
      'password2':"nottwo",
      'first_name':"two",
      'last_name':"two",
      'hospital':"1"
    })
    self.assertNotEqual(response.status_code, 302)   

    user = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    db.session.add(user)
    db.session.commit()
    # register with already existing email
    response = self.client.post(url_for('auth.register'), data = {
      'email':'one@one.com',
      'username':'two',
      'password':'two',
      'password2':'two',
      'first_name':"two",
      'last_name':"two",
      'hospital':"1"
    })    
    self.assertNotEqual(response.status_code,302)

    # register with already existing username
    response = self.client.post(url_for('auth.register'), data = {
      'email':'two@two.com',
      'username':'one',
      'password':'two',
      'password2':'two',
      'first_name':"two",
      'last_name':"two",
      'hospital':"1"
    })    
    self.assertNotEqual(response.status_code,302)    

    # register successfully
    response = self.client.post(url_for('auth.register'), data = {
      'email':'three@three.com',
      'username':'three',
      'password':'three',
      'password2':'three',
      'first_name':"three",
      'last_name':"three",
      'hospital':"Hospital1"
    },follow_redirects=True)
    data = response.get_data(as_text=True)    
    self.assertEqual(response.status_code,200)
    self.assertTrue('Successfully Registered' in data)
    user3 = User.query.filter_by(email='three@three.com').first()
    self.assertEqual(user3.email,'three@three.com')
    self.assertEqual(user3.username,'three')
    self.assertEqual(user3.first_name,'three')
    self.assertEqual(user3.last_name,'three')
    self.assertEqual(user3.hospital.name,'Hospital1')


  def test_auth_login_logout(self):
    # invalid email 
    response = self.client.post(url_for('auth.login'),data={
      'email':'notanemail',
      'password':'password'
    })
    self.assertNotEqual(response.status_code,302)
  
    # invalid password 
    response = self.client.post(url_for('auth.login'),data={
      'email':'one@one.com',
      'password':''
    })
    self.assertNotEqual(response.status_code,302)

    # unsuccessful login
    response = self.client.post(url_for('auth.login'), data= {
      'email':'usernotregistered@email.com',
      'password':'password'
    })
    self.assertNotEqual(response.status_code,302)
    self.assertTrue("Invalid Username or Password" in response.get_data(as_text=True))

    # successful login
    user = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    db.session.add(user)
    db.session.commit()
    response = self.client.post(url_for('auth.login'), data= {
      'email':'one@one.com',
      'password':'one'
    }, follow_redirects=True)
    self.assertEqual(response.status_code,200)
    self.assertTrue('Logged In Successfully' in response.get_data(as_text=True))

    # logout
    response = self.client.get(url_for('auth.logout'),follow_redirects=True)
    self.assertEqual(response.status_code,200)
    self.assertTrue('Successfully Logged Out' in response.get_data(as_text=True))

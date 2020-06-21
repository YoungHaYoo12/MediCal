import unittest
from app import create_app, db
from dateutil.relativedelta import relativedelta
from datetime import datetime

class FlaskClientTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client(use_cookies=True)

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
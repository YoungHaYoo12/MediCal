import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask_script import Manager,Shell
from flask_migrate import Migrate
from app import create_app, db, scheduler
from app.models import Hospital,User,Patient,PatientNote,Treatment,Appointment

app = create_app('default')
manager = Manager(app)
Migrate(app,db)

########################
#Context Processor SetUp
@app.context_processor
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
    def get_prev_year(year,month):
      curr = datetime(year=year,month=month,day=1)
      prev_year = curr - relativedelta(years=1)
      return prev_year
    def get_next_year(year,month):
      curr = datetime(year=year,month=month,day=1)
      next_year = curr + relativedelta(years=1)
      return next_year
    def get_next_week(year,month,day):
      curr = datetime(year=year,month=month,day=day)
      next_week = curr + relativedelta(weeks=1)
      return next_week
    def get_prev_week(year,month,day):
      curr = datetime(year=year,month=month,day=day)
      prev_week = curr - relativedelta(weeks=1)
      return prev_week
    def get_next_day(year,month,day):
      curr = datetime(year=year,month=month,day=day)
      next_day = curr + relativedelta(days=1)
      return next_day
    def get_prev_day(year,month,day):
      curr = datetime(year=year,month=month,day=day)
      prev_day = curr - relativedelta(days=1)
      return prev_day
    return dict(get_curr_date=get_curr_date,
                get_next_month=get_next_month,
                get_prev_month=get_prev_month,
                get_prev_year=get_prev_year,
                get_next_year=get_next_year,
                get_next_day=get_next_day,
                get_prev_day=get_prev_day,
                get_next_week=get_next_week,
                get_prev_week=get_prev_week
                )
########################
#Coverage SetUp
if os.environ.get('FLASK_COVERAGE'):
  import coverage
  COV = coverage.coverage(branch=True,include='app/*')
  COV.start()
########################

@manager.command
def test(coverage=False):
  """Run the Unit Tests"""
  if coverage and not os.environ.get('FLASK_COVERAGE'):
    import sys 
    os.environ['FLASK_COVERAGE'] = '1'
    os.execvp(sys.executable, [sys.executable] + sys.argv)

  import unittest
  tests = unittest.TestLoader().discover('tests')
  unittest.TextTestRunner(verbosity=2).run(tests)

  if COV:
    COV.stop()
    COV.save()
    print('Coverage Summary:')
    COV.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir,'tmp/coverage')
    COV.html_report(directory=covdir)
    print('HTML version: file://%s/index.html'%covdir)
    COV.erase()

# shell context for app
def make_shell_context():
  return dict(app=app,
              db=db,
              Hospital=Hospital,
              User=User,
              Patient=Patient,
              PatientNote=PatientNote,
              Appointment=Appointment,
              Treatment=Treatment)
manager.add_command("shell", Shell(make_context=make_shell_context))

# scheduled task for checking if appointments are going on
def scheduledTask():
  print("HI")

if __name__ == '__main__':
  #scheduler.add_job(id = 'Scheduled task', func = scheduledTask, trigger = 'interval',seconds=5)
  #scheduler.start()
  manager.run()
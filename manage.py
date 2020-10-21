import os
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand
from app import create_app, db
from app.models import Hospital,User,Patient,PatientNote,Treatment,Appointment,TreatmentTable,TreatmentTableEntry

app = create_app('default')
manager = Manager(app)
Migrate(app,db)
manager.add_command('db', MigrateCommand)

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
              Treatment=Treatment,
              TreatmentTable=TreatmentTable,
              TreatmentTableEntry=TreatmentTableEntry)
manager.add_command("shell", Shell(make_context=make_shell_context))

# scheduled task for checking if appointments are going on
def scheduledTask():
  print("HI")

if __name__ == '__main__':
  #scheduler.add_job(id = 'Scheduled task', func = scheduledTask, trigger = 'interval',seconds=5)
  #scheduler.start()
  manager.run()

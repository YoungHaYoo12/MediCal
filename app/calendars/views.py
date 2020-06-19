from flask import render_template, request, jsonify,redirect,url_for
from flask_login import current_user, login_required
from calendar import Calendar
import datetime
from app.calendars import calendars
from app.calendars.forms import AppointmentForm

cal = Calendar(7)

@calendars.route('/month/<int:year>/<int:month>',methods=['GET','POST'])
@login_required
def month(year,month):
  # form processing
  form = AppointmentForm()
  # treatment select field
  treatment_tuple = []
  treatments = current_user.hospital.treatments.all()
  for i in range(len(treatments)):
    treatment_tuple.append((str(treatments[i].id),treatments[i].name))
  form.treatment.choices = treatment_tuple

  # patient select field
  patient_tuple = []
  patients = current_user.patients.all()
  for i in range(len(patients)):
    patient_tuple.append((str(patients[i].id),patients[i].fullname))
  form.patient.choices = patient_tuple

  if form.validate_on_submit():
    print('appointment created!')
    return redirect(url_for('calendars.month',year=year,month=month))
  else:
    print('still trying')

  weeks = get_weeks(year,month)
  return render_template('calendars/month.html',form=form,weeks=weeks)

@calendars.route('/week/<int:year>/<int:month>/<int:week>')
def week(year,month,week):
  weeks = get_weeks(year,month)
  return render_template('calendars/week.html',week=weeks[week])

@calendars.route('/create/event',methods=['POST'])
def create_event():
  date_str = request.form['date']
  year = int(date_str[0:4])
  month = int(date_str[5:7])
  day = int(date_str[8:])
  date = datetime.date(year,month,day)
  print(date)


  return jsonify({
    'result':'success'
  })

####### HELPER FUNCTIONS #######
def get_weeks(year,month):
  month_days = []
  for day in cal.itermonthdates(int(year),month):
    month_days.append(day)
  weeks = [
    month_days[0:7],
    month_days[7:14],
    month_days[14:21],
    month_days[21:28],
    month_days[28:35]
  ]
  return weeks
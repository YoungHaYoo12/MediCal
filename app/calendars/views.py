from flask import render_template, request, jsonify,redirect,url_for,session
from flask_login import current_user, login_required
from calendar import Calendar
import datetime
from app import db
from app.calendars import calendars
from app.calendars.forms import AppointmentForm
from app.calendars.variables import num_to_month
from app.models import Appointment, Treatment, Patient

cal = Calendar(6)

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
    # create appointment instance
    appointment = Appointment(
      title=form.title.data,
      description=form.description.data,
      date_start=form.date_start.data,
      date_end=form.date_end.data
    )
    treatment = Treatment.query.get(int(form.treatment.data))
    patient = Patient.query.get(int(form.patient.data))
    appointment.treatment = treatment
    appointment.patient = patient
    appointment.user = current_user
    db.session.add(appointment)
    db.session.commit()

    return redirect(url_for('calendars.month',year=year,month=month))

  # calendar processing
  weeks = get_weeks(year,month)
  appointments = get_appointments_dict(weeks)

  return render_template('calendars/month.html',form=form,appointments=appointments,weeks=weeks,year_str=year,month_str=num_to_month[month])

@calendars.route('/week/<int:year>/<int:month>/<int:week>')
def week(year,month,week):
  weeks = get_weeks(year,month)
  return render_template('calendars/week.html',week=weeks[week])

@calendars.route('/appointment',methods=['POST'])
def appointment():
  appointment_id = request.form['appointment_id']
  appointment = Appointment.query.get_or_404(appointment_id)
  print(appointment.description)
  print(appointment.date_start)

  return jsonify({
    'result':'success',
    'appointment_id':appointment.id,
    'appointment_title':appointment.title,
    'appointment_description':appointment.description,
    'appointment_date_start':appointment.date_start,
    'appointment_date_end':appointment.date_end,
    'appointment_treatment_name':appointment.treatment.name,
    'appointment_patient_name':appointment.patient.fullname,
    'appointment_user_username':appointment.user.username,
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

def get_appointments_dict(weeks):
  result = {}
  for week in weeks:
    for day in week:
      appointments = Appointment.get_appointments(day.year,day.month,day.day).all()
      result[day] = appointments
  
  return result
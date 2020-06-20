from flask import render_template, request, jsonify,redirect,url_for,abort,flash
from flask_login import current_user, login_required
from calendar import Calendar
from app import db
from app.calendars import calendars
from app.calendars.forms import AppointmentForm
from app.calendars.variables import num_to_month
from app.models import Appointment, Treatment, Patient

cal = Calendar(6)

@calendars.route('/month/<int:year>/<int:month>',methods=['GET','POST'])
@login_required
def month(year,month):
  # validate url parameters
  if not validate_month(month) or not validate_year(year):
    abort(404)

  # form processing
  form = AppointmentForm()
  # treatment select field
  treatments = current_user.hospital.treatments.all()
  form.treatment.choices = get_treatment_tuple(treatments)

  # patient select field
  patients = current_user.patients.all()
  form.patient.choices = get_patient_tuple(patients)

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
    flash('Appointment Successfully Created')

    return redirect(url_for('calendars.month',year=year,month=month))

  # calendar processing
  weeks = get_weeks(year,month)
  appointments = get_appointments_dict(weeks)

  return render_template('calendars/month.html',form=form,appointments=appointments,weeks=weeks,year=year,num_to_month=num_to_month,month=month)

@calendars.route('/week/<int:year>/<int:month>/<int:week>')
def week(year,month,week):
  weeks = get_weeks(year,month)
  return render_template('calendars/week.html',week=weeks[week])

@calendars.route('/appointment',methods=['POST'])
@login_required
def appointment():
  appointment_id = request.form['appointment_id']
  appointment = Appointment.query.get_or_404(appointment_id)

  # validate User
  if not appointment in current_user.appointments.all():
    abort(403)

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

@calendars.route('/appointment/edit/<int:appointment_id>',methods=['GET','POST'])
@login_required
def appointment_edit(appointment_id):
  appointment = Appointment.query.get_or_404(appointment_id)

  # validate User
  if not appointment in current_user.appointments.all():
    abort(403)
  
  # form processing
  form = AppointmentForm()

  # treatment select field
  treatments = current_user.hospital.treatments.all()
  form.treatment.choices = get_treatment_tuple(treatments)

  # patient select field
  patients = current_user.patients.all()
  form.patient.choices = get_patient_tuple(patients)

  if form.validate_on_submit():
    # edit appointment instance
     appointment.title = form.title.data
     appointment.description = form.description.data
     appointment.date_start = form.date_start.data
     appointment.date_end = form.date_end.data
     treatment = Treatment.query.get(int(form.treatment.data))
     patient = Patient.query.get(int(form.patient.data))
     appointment.treatment = treatment
     appointment.patient = patient
     db.session.commit()
     flash('Appointment Successfully Edited')

     # redirect to calendars.month
     year = appointment.date_start.year
     month = appointment.date_start.month
     return redirect(url_for('calendars.month',year=year,month=month))
  elif request.method == 'GET':
    form.title.data = appointment.title
    form.description.data = appointment.description
    form.date_start.data = appointment.date_start
    form.date_end.data = appointment.date_end
    form.treatment.data = str(appointment.treatment.id)
    form.patient.data = str(appointment.patient.id)

  return render_template('calendars/edit.html',form=form)

@calendars.route('/appointment/delete/<int:appointment_id>')
@login_required
def appointment_delete(appointment_id):
  appointment = Appointment.query.get_or_404(appointment_id)
  year = appointment.date_start.year
  month = appointment.date_start.month

  # validate User
  if not appointment in current_user.appointments.all():
    abort(403)
  
  # delete appointment
  db.session.delete(appointment)
  db.session.commit()

  flash('Appointment Successfully Deleted')
  
  return redirect(url_for('calendars.month',year=year,month=month))

    
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

def validate_year(year):
  return year >= 2 and year <= 9998

def validate_month(month):
  return month <= 12 and month >= 1

def get_appointments_dict(weeks):
  result = {}
  for week in weeks:
    for day in week:
      appointments = Appointment.get_appointments(day.year,day.month,day.day).all()
      result[day] = appointments
  
  return result

def get_treatment_tuple(treatments):
  treatment_tuple = []
  for i in range(len(treatments)):
    treatment_tuple.append((str(treatments[i].id),treatments[i].name))
  return treatment_tuple

def get_patient_tuple(patients):
  patient_tuple = []
  for i in range(len(patients)):
    patient_tuple.append((str(patients[i].id),patients[i].fullname))
  return patient_tuple
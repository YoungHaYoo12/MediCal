from flask import render_template, request, jsonify,redirect,url_for,abort,flash,session
from flask_login import current_user, login_required
from app import db
from app.appointments import appointments
from app.appointments.forms import AppointmentForm, AppointmentFilterForm
from app.calendars.functions import get_weeks, validate_month, validate_year
from app.calendars.variables import num_to_month
from app.models import Appointment, Treatment, Patient, User

@appointments.route('/list/<int:year>/<int:month>',methods=['GET','POST'])
@login_required
def list(year,month,user_id=None,patient_email=None,treatment_name=None):
  # validate url parameters
  if not validate_month(month) or not validate_year(year):
    abort(404)

  # form 1 processing
  form = AppointmentForm()
  # treatment select field
  treatments = current_user.hospital.treatments.all()
  form.treatment.choices = get_treatment_tuple(treatments)
  # patient select field
  patients = current_user.patients.all()
  form.patient.choices = get_patient_tuple(patients)

  # form 2 processing
  form2 = AppointmentFilterForm()
  # user select field 
  users = current_user.hospital.users.all()
  user_tuple = get_user_tuple(users)
  form2.user.choices = user_tuple

  if form.validate_on_submit() and form.submit.data:
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

    return redirect(url_for('appointments.list',year=year,month=month))

  elif form2.validate_on_submit() and form2.filter.data:
    session['user_id'] = form2.user.data
    session['patient_email'] = form2.patient.data
    session['treatment_name'] = form2.treatment.data
    return redirect(url_for('appointments.list',year=year,month=month))
  elif request.method == 'GET':
    form2.user.data = session.get('user_id')
    form2.patient.data = session.get('patient_email')
    form2.treatment.data = session.get('treatment_name')
  
  # CALENDAR PROCESSING
  # default arguments (before filtering)
  user = current_user
  patient = None
  treatment = None
  messages = []

  # retrieve user,patient,treatment from filtering form information
  if session.get('user_id') is not None:
    user = User.query.get_or_404(int(session.get('user_id')))
  if session.get('patient_email') is not None and len(session.get('patient_email')) != 0:
    patient = Patient.query.filter_by(email=session.get('patient_email')).first()
    if patient is None:
      messages.append('Patient Email Not Valid')
  if session.get('treatment_name') is not None and len(session.get('treatment_name')) != 0:
    treatment = Treatment.query.filter_by(name=session.get('treatment_name')).first()
    if treatment is None:
      messages.append('Treatment Name Not Valid')
    
  weeks = get_weeks(year,month)
  appointments = get_appointments_dict(user=user,patient=patient,treatment=treatment,weeks=weeks)

  return render_template('appointments/list.html',form=form,form2=form2,appointments=appointments,weeks=weeks,year=year,month=month,num_to_month=num_to_month,messages=messages)

@appointments.route('/appointment',methods=['POST'])
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

@appointments.route('/delete/<int:appointment_id>')
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
  
  return redirect(url_for('appointments.list',year=year,month=month))

@appointments.route('/edit/<int:appointment_id>',methods=['GET','POST'])
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

     year = appointment.date_start.year
     month = appointment.date_start.month
     return redirect(url_for('appointments.list',year=year,month=month))
  elif request.method == 'GET':
    form.title.data = appointment.title
    form.description.data = appointment.description
    form.date_start.data = appointment.date_start
    form.date_end.data = appointment.date_end
    form.treatment.data = str(appointment.treatment.id)
    form.patient.data = str(appointment.patient.id)

  return render_template('appointments/edit.html',form=form)


####### HELPER FUNCTIONS #######
def get_appointments_dict(weeks,user=None,patient=None,treatment=None,hospital=None,title=None):
  result = {}
  for week in weeks:
    for day in week:
      appointments = Appointment.get_filtered_appointments(day.year,day.month,day.day,user,patient,treatment,hospital,title).all()
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

def get_user_tuple(users):
  user_tuple = []
  for i in range(len(users)):
    user_tuple.append((str(users[i].id),users[i].username))
  return user_tuple
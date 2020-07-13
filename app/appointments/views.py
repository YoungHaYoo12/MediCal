from datetime import datetime
from flask import render_template, request,redirect,url_for,abort,flash,session,jsonify
from flask_login import current_user, login_required
from app import db
from app.appointments import appointments
from app.appointments.forms import AppointmentForm, AppointmentFilterForm
from app.models import Appointment, Treatment, Patient, User

@appointments.route('/list',methods=['GET','POST'])
@login_required
def list():
  # form processing
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
  user_tuple.append(('all','All'))  
  form2.user.choices = user_tuple
  # patient select field
  patients = current_user.hospital.get_patients().all()
  patient_tuple = get_patient_tuple(patients)
  patient_tuple.append(('all','All'))
  form2.patient.choices = patient_tuple
  # treatment select field
  treatments = current_user.hospital.treatments.all()
  treatment_tuple = get_treatment_tuple(treatments)
  treatment_tuple.append(('all','All'))
  form2.treatment.choices = treatment_tuple

  if form.submit.data and form.validate_on_submit():
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
    appointment.color = form.color.data
    db.session.add(appointment)
    db.session.commit()
    flash('Appointment Successfully Created')

    return redirect(url_for('appointments.list'))
  elif form2.submit2.data and form2.validate_on_submit():
    session['user'] = form2.user.data
    session['patient'] = form2.patient.data
    session['treatment'] = form2.treatment.data
    return redirect(url_for('appointments.list'))
    
  form.date_start.data = datetime.utcnow()
  form.date_end.data = datetime.utcnow()
  if session.get('user') is None:
    form2.user.data = 'all'
  else:
    form2.user.data = session.get('user')
  if session.get('patient') is None:
    form2.patient.data = 'all'
  else:
    form2.patient.data = session.get('patient')
  if session.get('treatment') is None:
    form2.treatment.data = 'all'
  else:
    form2.treatment.data = session.get('treatment')


  return render_template('appointments/list.html',form=form,form2=form2)

@appointments.route('/move-appointment',methods=['POST'])
@login_required
def move_appointment():
  appointment_id = request.form['appointment_id']
  appointment = Appointment.query.get_or_404(appointment_id)

  # validate User
  if not appointment.user in current_user.hospital.users.all():
    abort(403)
  
  # modify event model
  appointment.date_start = datetime.fromisoformat(request.form['start'])
  if len(request.form['end']) == 0:
    appointment.date_start = datetime.fromisoformat(request.form['start'])
  else:
    appointment.date_end = datetime.fromisoformat(request.form['end'])
  db.session.commit()
  print(appointment.date_start)
  print(appointment.date_end)

  return jsonify({
    'result':'success'
  })

@appointments.route('/data',methods=['POST'])
@login_required
def data():
  # appointment retrieval for user and patient pages 
  model = request.form.get('model')
  model_id = request.form.get('model_id')
  if model and model_id:
    if model == 'user':
      user = User.query.get_or_404(model_id)
      appointments = user.appointments.all()
    elif model == 'patient':
      patient = Patient.query.get_or_404(model_id)
      appointments = patient.appointments.all()
    else:
      abort(404)

  # appointment retrieval for appointments.list page
  else:
    appointments = current_user.hospital.get_appointments().all()

  # parsing into appointments_data
  appointments_data = []
  for appointment in appointments:
    appointments_data.append({
      'id':appointment.id,
      'title':appointment.title,
      'start':appointment.date_start.isoformat(),
      'end':appointment.date_end.isoformat(),
      'allDay':"false",
      'color':appointment.color,
      'user_id':appointment.user.id,
      'patient_id':appointment.patient.id,
      'treatment_id':appointment.treatment.id,
      'hospital_id':appointment.user.hospital.id
    })

  return jsonify({
    'result':'success',
    'appointments_data':appointments_data
  })

@appointments.route('/appointment',methods=['POST'])
@login_required
def appointment():
  appointment_id = request.form['appointment_id']
  appointment = Appointment.query.get_or_404(appointment_id)

  # validate User
  if not appointment.user in current_user.hospital.users.all():
    abort(403)
    
  return jsonify({
    'result':'success',
    'user_is_appointment_owner':appointment.user == current_user,
    'appointment_id':appointment.id,
    'appointment_title':appointment.title,
    'appointment_description':appointment.description,
    'appointment_date_start':appointment.date_start,
    'appointment_date_end':appointment.date_end,
    'appointment_treatment_name':appointment.treatment.name,
    'appointment_patient_name':appointment.patient.fullname,
    'appointment_user_username':appointment.user.username,
    'patient_id':appointment.patient.id,
    'user_username':appointment.user.username
  })

@appointments.route('/delete/<int:appointment_id>')
@login_required
def appointment_delete(appointment_id):
  appointment = Appointment.query.get_or_404(appointment_id)

  # validate User
  if not appointment in current_user.appointments.all():
    abort(403)
  
  # delete appointment
  db.session.delete(appointment)
  db.session.commit()

  flash('Appointment Successfully Deleted')
  
  return redirect(url_for('appointments.list'))

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
     appointment.color = form.color.data
     treatment = Treatment.query.get(int(form.treatment.data))
     patient = Patient.query.get(int(form.patient.data))
     appointment.treatment = treatment
     appointment.patient = patient
     db.session.commit()
     flash('Appointment Successfully Edited')

     return redirect(url_for('appointments.list'))
  elif request.method == 'GET':
    form.title.data = appointment.title
    form.description.data = appointment.description
    form.date_start.data = appointment.date_start
    form.date_end.data = appointment.date_end
    form.treatment.data = str(appointment.treatment.id)
    form.patient.data = str(appointment.patient.id)
    form.color.data = str(appointment.color)

  return render_template('appointments/edit.html',form=form)

@appointments.route('/is_completed/<int:appointment_id>')
@login_required
def toggle_is_completed(appointment_id):
  appointment = Appointment.query.get_or_404(appointment_id)

  # validate user
  if appointment.user != current_user:
    abort(403)
  
  appointment.is_completed = not appointment.is_completed
  db.session.add(appointment)
  db.session.commit()

  return redirect(url_for('appointments.list_month',year=appointment.date_start.year,month=appointment.date_start.month))

####### HELPER FUNCTIONS #######
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
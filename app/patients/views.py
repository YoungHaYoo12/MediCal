from flask import render_template,request,redirect,flash,url_for,abort
from flask_login import login_required,current_user
from app import db
from app.models import Patient, User
from app.patients import patients
from app.patients.forms import PatientAddForm, PatientEditForm,AddDoctorForm

@patients.route('/list/<category>',methods=['GET','POST'])
@login_required
def list(category=None):
  page = request.args.get('page',1,type=int)
  
  # retrieve patients of user or hospital
  if category == "hospital":
    query = current_user.hospital.get_patients()  
  elif category == "user":
    query = current_user.patients.order_by(Patient.last_name.asc())
  else:
    abort(404)
  
  pagination = query.paginate(page,per_page=10)
  patients = pagination.items

  # form processing
  form = PatientAddForm()

  if form.validate_on_submit():
    # create new patient
    patient = Patient(first_name=form.first_name.data,
                      last_name=form.last_name.data,
                      email=form.email.data)
    current_user.patients.append(patient)
    db.session.add(patient)
    db.session.commit()

    flash('New Patient Added')
    return redirect(url_for('patients.list',category='user'))

  return render_template('patients/list.html',patients=patients,pagination=pagination,form=form,category=category)

@patients.route('/patient/<int:id>')
@login_required
def patient(id):
  # confirm that patient is connected to current_user
  patient = Patient.query.get_or_404(id)
  if not patient in current_user.patients.all():
    abort(403)
  
  return render_template('patients/patient.html',patient=patient)

@patients.route('/delete/<int:id>')
@login_required
def delete(id):
  # confirm that patient is connected to current_user
  patient = Patient.query.get_or_404(id)
  if not patient in current_user.patients.all():
    abort(403)

  db.session.delete(patient)
  db.session.commit()

  flash('Patient Successfully Deleted')
  return redirect(url_for('patients.list',category='user'))

@patients.route('/edit/<int:id>',methods=['POST','GET'])
@login_required
def edit(id):
  # form processing
  form = PatientEditForm()

  # confirm that patient is connected to current_user
  patient = Patient.query.get_or_404(id)
  if not patient in current_user.patients.all():
    abort(403)

  if form.validate_on_submit():
    patient.first_name = form.first_name.data
    patient.last_name = form.last_name.data
    patient.email = form.email.data
    db.session.commit()
    flash('Patient Edit Successful')
    return redirect(url_for('patients.patient',id=patient.id))
  elif request.method == 'GET':
    form.first_name.data = patient.first_name
    form.last_name.data = patient.last_name
    form.email.data = patient.email

  return render_template('patients/edit.html',form=form,patient=patient)

@patients.route('/add_doctor/<int:patient_id>',methods=['GET','POST'])
@login_required
def add_doctor(patient_id):
  # confirm that patient is connected to current_user
  patient = Patient.query.get_or_404(patient_id)
  if not patient in current_user.patients.all():
    abort(403)

  # form processing
  form = AddDoctorForm()
  users = current_user.hospital.users.all()
  form.doctor.choices = get_user_tuple(users)

  if form.validate_on_submit():
    user_to_add = User.query.get_or_404(form.doctor.data)

    if patient in user_to_add.patients.all():
      flash('Patient Already Connected to User')
      return redirect(url_for('patients.patient',id=patient.id))

    patient.users.append(user_to_add)
    db.session.commit()

    flash('Doctor Successfully Added To Patient')
    return redirect(url_for('patients.patient',id=patient.id))
  
  return render_template('patients/add_doctor.html',form=form)

####### HELPER FUNCTIONS #######
def get_user_tuple(users):
  user_tuple = []
  for i in range(len(users)):
    user_tuple.append((str(users[i].id),users[i].username))
  return user_tuple
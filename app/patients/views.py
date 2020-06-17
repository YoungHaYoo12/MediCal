from flask import render_template,request,redirect,flash,url_for,abort
from flask_login import login_required,current_user
from app import db
from app.models import User, Patient,relationships
from app.patients import patients
from app.patients.forms import PatientAddForm, PatientEditForm

@patients.route('/list/<category>',methods=['GET','POST'])
@login_required
def list(category=None):
  page = request.args.get('page',1,type=int)
  
  # retrieve patients of user or hospital
  if category == "hospital":
    query = Patient.query.join(relationships,relationships.columns.patient_id==Patient.id).join(User,relationships.columns.user_id==User.id).filter(User.hospital_id == current_user.hospital_id).order_by(Patient.last_name.asc())    
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

  flash('Patient Succesfully Deleted')
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
    flash('User Edit Successful')
    return redirect(url_for('patients.patient',id=patient.id))
  elif request.method == 'GET':
    form.first_name.data = patient.first_name
    form.last_name.data = patient.last_name
    form.email.data = patient.email

  return render_template('patients/edit.html',form=form,patient=patient)
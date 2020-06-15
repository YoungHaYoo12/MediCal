from flask import render_template,request,redirect,flash,url_for,abort
from flask_login import login_required,current_user
from app import db
from app.models import User, Patient
from app.patients import patients
from app.patients.forms import PatientAddForm

@patients.route('/user_list/<username>')
@login_required
def list(username):
  page = request.args.get('page',1,type=int)
  
  # retrieve user
  user = User.query.filter_by(username=username).first_or_404()

  # retrieve patients of user
  query = user.patients.order_by(Patient.last_name.asc())
  pagination = query.paginate(page,per_page=10)
  patients = pagination.items

  return render_template('patients/list.html',patients=patients,pagination=pagination)

@patients.route('/add',methods=['GET','POST'])
@login_required
def add():
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
    return redirect(url_for('patients.list',username=current_user.username))
  
  return render_template('patients/add.html',form=form)

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
  return redirect(url_for('patients.list',username=current_user.username))
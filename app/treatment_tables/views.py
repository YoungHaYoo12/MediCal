from flask import render_template, redirect, url_for,flash,abort,request
from flask_login import current_user, login_required
from app import db
from app.models import Treatment,TreatmentTable, TreatmentTableEntry, Patient
from app.appointments.views import get_treatment_tuple
from app.treatment_tables.forms import TreatmentTableAddForm,TreatmentTableEditForm,TreatmentTableEntryAddForm

from app.treatment_tables import treatment_tables

@treatment_tables.route('/list/<int:patient_id>')
@login_required
def list(patient_id):
  # retrieve and validate patient
  patient = Patient.query.get_or_404(patient_id)
  if not patient in current_user.patients.all():
    abort(403)
  
  # retrieve treatment tables for patient
  page = request.args.get('page',1,type=int)
  pagination = patient.treatment_tables.order_by(TreatmentTable.name).paginate(page=page,per_page=10)
  treatment_tables = pagination.items

  return render_template('treatment_tables/list.html',patient=patient,treatment_tables=treatment_tables,pagination=pagination)

@treatment_tables.route('/<int:treatment_table_id>',methods=['GET','POST'])
@login_required
def table(treatment_table_id):
  # retrieve and validate treatment table
  table = TreatmentTable.query.get_or_404(treatment_table_id)
  patient = table.patient
  if not patient in current_user.patients.all():
    abort(403)

  # form processing
  form = TreatmentTableEntryAddForm()
  treatments = current_user.hospital.treatments.all()
  form.treatment.choices = get_treatment_tuple(treatments)

  if form.validate_on_submit():
    treatment = Treatment.query.get_or_404(form.treatment.data)
    entry = TreatmentTableEntry(treatment=treatment,treatment_table=table,timestamp=form.date.data,amount=form.amount.data,note=form.note.data)
    db.session.add(entry)
    db.session.commit()

    flash('Entry Successfuly Added')
    return redirect(url_for('treatment_tables.table',treatment_table_id=table.id))

  return render_template('treatment_tables/table.html',table=table,form=form)

@treatment_tables.route('/add_table/<int:patient_id>',methods=['GET','POST'])
@login_required
def add_table(patient_id):
  # retrieve and validate patient
  patient = Patient.query.get_or_404(patient_id)
  if not patient in current_user.patients.all():
    abort(403)
  
  # form processing
  form = TreatmentTableAddForm()

  if form.validate_on_submit():
    table = TreatmentTable(name=form.name.data)
    table.patient = patient
    db.session.add(table)
    db.session.commit()
    flash('Treatment Table Successfully Added')
    return redirect(url_for('treatment_tables.list',patient_id=patient_id))

  return render_template('treatment_tables/add_table.html',form=form,patient=patient)

@treatment_tables.route('/edit_table/<int:treatment_table_id>',methods=['GET','POST'])
@login_required
def edit_table(treatment_table_id):
  # retrieve and validate treatment table
  table = TreatmentTable.query.get_or_404(treatment_table_id)
  patient = table.patient
  if not patient in current_user.patients.all():
    abort(403)
  
  # form processing
  form = TreatmentTableEditForm()

  if form.validate_on_submit():
    table.name = form.name.data
    db.session.commit()
    flash('Treatment Table Successfully Edited')
    return redirect(url_for('treatment_tables.list',patient_id=patient.id))
    
  elif request.method == 'GET':
    form.name.data = table.name
  
  return render_template('treatment_tables/add_table.html',form=form,patient=patient)


@treatment_tables.route('/delete_table/<int:treatment_table_id>')
@login_required
def delete_table(treatment_table_id):
  # retrieve and validate treatment table 
  table = TreatmentTable.query.get_or_404(treatment_table_id)
  patient = table.patient
  if not patient in current_user.patients.all():
    abort(403)
  
  db.session.delete(table)
  db.session.commit()

  flash('Treatment Table Successfully Deleted')

  return redirect(url_for('treatment_tables.list',patient_id=patient.id))

@treatment_tables.route('/add_entry/<int:treatment_table_id>',methods=['GET','POST'])
@login_required
def add_entry(treatment_table_id):
  # retrieve and validate treatment table 
  table = TreatmentTable.query.get_or_404(treatment_table_id)
  patient = table.patient
  if not patient in current_user.patients.all():
    abort(403)
  
  # form processing
  form = TreatmentTableEntryAddForm()
  treatments = current_user.hospital.treatments.all()
  form.treatment.choices = get_treatment_tuple(treatments)

  if form.validate_on_submit():
    entry = TreatmentTableEntry()
    db.session.add(entry)
    db.session.commit()
    flash('Entry Successfully Added')
    return redirect(url_for('treatment_tables.table',treatment_table_id=table.id))
  
  return render_template('treatment_tables/add_entry.html',form=form)
  
@treatment_tables.route('/delete_entry/<int:treatment_entry_id>')
@login_required
def delete_entry(treatment_entry_id):
  # retrieve and validate treatment entry
  entry = TreatmentTableEntry.query.get_or_404(treatment_entry_id)
  table = entry.treatment_table
  patient = table.patient

  if not patient in current_user.patients.all():
    abort(403)
  
  # delete entry
  db.session.delete(entry)
  db.session.commit()

  flash('Entry Successfully Deleted')
  return redirect(url_for('treatment_tables.table',treatment_table_id=table.id))
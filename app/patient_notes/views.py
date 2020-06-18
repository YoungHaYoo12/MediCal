from flask import render_template,abort,flash,redirect,url_for,request
from flask_login import login_required, current_user
from app import db
from app.patient_notes import patient_notes
from app.patient_notes.forms import PatientNoteAddForm
from app.models import Patient, PatientNote

@patient_notes.route('/patient/<int:patient_id>')
@login_required
def list(patient_id):
  # validate patient
  patient = Patient.query.get_or_404(patient_id)
  if not patient in current_user.patients.all():
    abort(403)  

  # Retrive patient notes
  page = request.args.get('page',1,type=int)
  pagination = patient.patient_notes.order_by(PatientNote.date_modified.desc()).paginate(page=page,per_page=10)
  patient_notes = pagination.items;

  return render_template('patient_notes/list.html',
  patient_notes=patient_notes,pagination=pagination,patient=patient)

@patient_notes.route('/patient_note/<int:patient_note_id>')
@login_required
def patient_note(patient_note_id):
  # retrieve patient note, patient, user
  patient_note = PatientNote.query.get_or_404(patient_note_id)
  patient = patient_note.patient
  user = patient_note.user

  # validate user's access
  if not patient in current_user.patients.all():
    abort(403)
  
  return render_template('patient_notes/patient_note.html',patient_note=patient_note,patient=patient,user=user)

@patient_notes.route('/add/<int:patient_id>',methods=['GET','POST'])
@login_required
def add(patient_id):
  # validate patient
  patient = Patient.query.get_or_404(patient_id)
  if not patient in current_user.patients.all():
    abort(403)  
  
  # form processing
  form = PatientNoteAddForm()
  if form.validate_on_submit():
    patient_note = PatientNote(title=form.title.data, notes=form.notes.data)
    patient_note.patient = patient
    patient_note.user = current_user
    db.session.add(patient_note)
    db.session.commit()
    flash('Patient Note Successfully Posted.')
    return redirect(url_for('patient_notes.list',patient_id=patient_id))
  
  return render_template('patient_notes/add.html',form=form,patient=patient)

@patient_notes.route('/edit/<int:patient_note_id>', methods=['GET','POST'])
@login_required
def edit(patient_note_id):
  # validate current user
  patient_note = PatientNote.query.get_or_404(patient_note_id)
  if current_user != patient_note.user:
    abort(403)
  
  # form processing
  form = PatientNoteAddForm()
  if form.validate_on_submit():
    patient_note.title = form.title.data
    patient_note.notes = form.notes.data
    patient_note.refresh()
    db.session.commit()
    flash('Patient Note Successfully Edited')
    return redirect(url_for('patient_notes.patient_note',patient_note_id=patient_note.id))
  elif request.method == 'GET':
    form.title.data = patient_note.title
    form.notes.data = patient_note.notes
  
  return render_template('patient_notes/add.html',form=form,patient=patient_note.patient)
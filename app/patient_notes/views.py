from flask import render_template,abort
from flask_login import login_required, current_user
from app.patient_notes import patient_notes
from app.models import Patient

@patient_notes.route('/patient/<int:patient_id>')
@login_required
def list(patient_id):
  # validate patient
  patient = Patient.query.get_or_404(patient_id)
  if not patient in current_user.patients.all():
    abort(403)  

  patient_notes = patient.patient_notes.all()

  return render_template('patient_notes/list.html',
  patient_notes=patient_notes,patient=patient)
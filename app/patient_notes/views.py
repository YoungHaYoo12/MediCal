from flask import render_template
from flask_login import login_required
from app.patient_notes import patient_notes
from app.models import Patient

@patient_notes.route('/patient/<int:patient_id>')
@login_required
def list(id):
  # retrive patient_notes if patient exists
  patient = Patient.query.get_or_404(patient_id)
  patient_notes = patient.patient_notes.all()

  return render_template('patient_notes/list.html',
  patient_notes=patient_notes,patient=patient)
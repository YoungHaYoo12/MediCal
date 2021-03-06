import unittest
from sqlalchemy.exc import IntegrityError
from app import create_app, db
from app.models import Appointment, Patient, User, Treatment, TreatmentTable, TreatmentTableEntry,PatientNote,Hospital
from datetime import datetime,timedelta

class FlaskTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

class TreatmentTableModelTestCase(FlaskTestCase):
  def test_id(self):
    table = TreatmentTable(name='Table 1')
    db.session.add(table)
    db.session.commit()
    self.assertEqual(table.id, 1)
    
  def test_attributes_assignment(self):
    self.assertEqual(TreatmentTable.__tablename__,'treatment_tables')
    patient = Patient(first_name='John',last_name='Doe',email='johndoe@example.com')
    table = TreatmentTable(name='Table 1',patient=patient)

    self.assertEqual(table.name,'Table 1')
    self.assertEqual(table.patient,patient)

class TreatmentTableEntryModelTestCase(FlaskTestCase):
  def test_id(self):
    entry = TreatmentTableEntry()
    db.session.add(entry)
    db.session.commit()
    self.assertEqual(entry.id, 1)

  def test_attributes_assignment(self):
    date = datetime.utcnow()
    amount = "1 mg Dose"
    note = "Additional Note"
    treatment = Treatment(name='Treatment 1')
    patient = Patient(first_name='John',last_name='Doe',email='johndoe@example.com')
    table = TreatmentTable(name='Table 1',patient=patient)

    entry = TreatmentTableEntry(timestamp=date,amount=amount,note=note,treatment=treatment,treatment_table=table)
    
    self.assertEqual(entry.timestamp,date)
    self.assertEqual(entry.amount,'1 mg Dose')
    self.assertEqual(entry.note,"Additional Note")
    self.assertEqual(entry.treatment,treatment)
    self.assertEqual(entry.treatment_table,table)

class ModelRelationshipsTestCase(FlaskTestCase):
  def test_treatment_table_entry_treatment_relationship(self):
    entry1 = TreatmentTableEntry()
    entry2 = TreatmentTableEntry()

    treatment1 = Treatment(name='Treatment 1')
    treatment2 = Treatment(name='Treatment 2')

    # before connecting
    self.assertEqual(len(treatment1.treatment_table_entries.all()),0)
    self.assertEqual(len(treatment2.treatment_table_entries.all()),0)

    # after connecting
    entry1.treatment = treatment1
    entry2.treatment = treatment1
    
    self.assertEqual(len(treatment1.treatment_table_entries.all()),2)
    self.assertEqual(treatment1,entry1.treatment)
    self.assertEqual(treatment1,entry2.treatment)
    self.assertTrue(entry1 in treatment1.treatment_table_entries.all())
    self.assertTrue(entry2 in treatment1.treatment_table_entries.all())

    self.assertEqual(len(treatment2.treatment_table_entries.all()),0)
    self.assertNotEqual(treatment2,entry1.treatment)
    self.assertNotEqual(treatment2,entry2.treatment)
    self.assertFalse(entry1 in treatment2.treatment_table_entries.all())
    self.assertFalse(entry2 in treatment2.treatment_table_entries.all())

  def test_patient_treatment_table_relationship(self):
    patient1 = Patient(first_name='Patient',last_name='1',email='patient1@example.com')
    patient2 = Patient(first_name='Patient',last_name='2',email='patient2@example.com')

    table1 = TreatmentTable(name='Table 1')
    table2 = TreatmentTable(name='Table 2')

    # before connecting
    self.assertEqual(len(patient1.treatment_tables.all()),0)
    self.assertEqual(len(patient2.treatment_tables.all()),0)

    # after connecting
    table1.patient = patient1
    table2.patient = patient1
    
    self.assertEqual(len(patient1.treatment_tables.all()),2)
    self.assertEqual(patient1,table1.patient)
    self.assertEqual(patient1,table2.patient)
    self.assertTrue(table1 in patient1.treatment_tables.all())
    self.assertTrue(table2 in patient1.treatment_tables.all())

    self.assertEqual(len(patient2.treatment_tables.all()),0)
    self.assertNotEqual(patient2,table1.patient)
    self.assertNotEqual(patient2,table2.patient)
    self.assertFalse(table1 in patient2.treatment_tables.all())

  def test_treatment_table_treatment_table_entry_relationship(self):
    table1 = TreatmentTable(name='Table 1')
    table2 = TreatmentTable(name='Table 2')

    entry1 = TreatmentTableEntry()
    entry2 = TreatmentTableEntry()

    # before connecting
    self.assertEqual(len(table1.treatment_table_entries.all()),0)
    self.assertEqual(len(table2.treatment_table_entries.all()),0)

    # after connecting
    entry1.treatment_table = table1
    entry2.treatment_table = table1
    self.assertEqual(len(table1.treatment_table_entries.all()),2)
    self.assertEqual(table1,entry1.treatment_table)
    self.assertEqual(table1,entry2.treatment_table)
    self.assertTrue(entry1 in table1.treatment_table_entries.all())
    self.assertTrue(entry2 in table1.treatment_table_entries.all())

    self.assertEqual(len(table2.treatment_table_entries.all()),0)
    self.assertNotEqual(table2,entry1.treatment_table)
    self.assertNotEqual(table2,entry2.treatment_table)
    self.assertFalse(entry1 in table2.treatment_table_entries.all())
    self.assertFalse(entry2 in table2.treatment_table_entries.all())    


  def test_database_cascade(self):
    # User and PatientNote
    user = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    patient_note = PatientNote(title='title',notes='notes')
    patient_note.user = user
    db.session.add_all([user,patient_note])
    db.session.commit()
    db.session.delete(user)
    db.session.commit()
    self.assertEqual(len(PatientNote.query.all()), 0)

    # User and Appointment
    user = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    today = datetime.utcnow()
    appointment = Appointment(title='title',description='description',date_start=today,date_end=today)
    appointment.user = user
    db.session.add_all([user,appointment])
    db.session.commit()
    db.session.delete(user)
    db.session.commit()
    self.assertEqual(len(Appointment.query.all()), 0)

    # Patient and PatientNote
    patient = Patient(first_name='patient1',last_name='patient1',email='patient1@gmail.com')
    patient_note = PatientNote(title='title',notes='notes')
    patient_note.patient = patient
    db.session.add_all([patient,patient_note])
    db.session.commit()
    db.session.delete(patient)
    db.session.commit()
    self.assertEqual(len(PatientNote.query.all()), 0)

    # Patient and Appointment
    patient = Patient(first_name='patient1',last_name='patient1',email='patient1@gmail.com')
    appointment = Appointment(title='title',description='description',date_start=today,date_end=today)
    appointment.patient = patient
    db.session.add_all([patient,appointment])
    db.session.commit()
    db.session.delete(patient)
    db.session.commit()
    self.assertEqual(len(Appointment.query.all()), 0)

    # Treatment and Appointment
    treatment = Treatment(name='treatment1')
    appointment = Appointment(title='title',description='description',date_start=today,date_end=today)
    appointment.treatment = treatment
    db.session.add_all([treatment,appointment])
    db.session.commit()
    db.session.delete(treatment)
    db.session.commit()
    self.assertEqual(len(Appointment.query.all()), 0)

    # Hospital and User
    user = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    hospital = Hospital(name='hospital')
    user.hospital = hospital
    db.session.add_all([hospital,user])
    db.session.commit()
    db.session.delete(hospital)
    db.session.commit()
    self.assertEqual(len(User.query.all()), 0)

    # Hospital and Treatment
    treatment = Treatment(name='treatment1')
    hospital = Hospital(name='hospital')
    treatment.hospital = hospital
    db.session.add_all([hospital,treatment])
    db.session.commit()
    db.session.delete(hospital)
    db.session.commit()
    self.assertEqual(len(Treatment.query.all()), 0)

    # TreatmentTable and TreatmentTableEntry
    table = TreatmentTable(name='table')
    entry = TreatmentTableEntry()
    entry.treatment_table = table
    db.session.add_all([table,entry])
    db.session.commit()
    db.session.delete(table)
    db.session.commit()
    self.assertEqual(len(TreatmentTableEntry.query.all()), 0)

    # TreatmentTable and Patient
    table = TreatmentTable(name='table')
    patient = Patient(first_name='patient1',last_name='patient1',email='patient1@gmail.com')
    table.patient = patient
    db.session.add_all([table,patient])
    db.session.commit()
    db.session.delete(patient)
    db.session.commit()
    self.assertEqual(len(TreatmentTable.query.all()), 0)

    # TreatmentTableEntry and Treatment
    treatment = Treatment(name='treatment')
    entry = TreatmentTableEntry()
    entry.treatment = treatment
    db.session.add_all([treatment,entry])
    db.session.commit()
    db.session.delete(treatment)
    db.session.commit()
    self.assertEqual(len(TreatmentTableEntry.query.all()), 0)

class TreatmentModelTestCase(FlaskTestCase):
  def test_id(self):
    treatment = Treatment(name='medicine')
    db.session.add(treatment)
    db.session.commit()
    self.assertEqual(treatment.id, 1)

  def test_repr(self):
    treatment = Treatment(name='therapy')
    self.assertEqual(treatment.__repr__(), 'therapy')

  def test_name_assignment(self):
    treatment = Treatment(name='medicine')
    self.assertEqual(treatment.name,'medicine')

class PatientModelTestCase(FlaskTestCase):
  def test_id(self):
    patient = Patient(first_name='John',last_name='Doe',email='johndoe@example.com')
    db.session.add(patient)
    db.session.commit()
    self.assertEqual(patient.id, 1)

  def test_repr(self):
    patient = Patient(first_name='John',last_name='Doe',email='johndoe@example.com')
    self.assertEqual(patient.__repr__(), 'John Doe')

  def test_name_assignment(self):
    patient = Patient(first_name='John',last_name='Doe',email='johndoe@example.com')
    self.assertEqual(patient.first_name,'John')
    self.assertEqual(patient.last_name,'Doe')
    self.assertEqual(patient.fullname,'John Doe')

  def test_email_assignment(self):
    patient = Patient(first_name='John',last_name='Doe',email='johndoe@example.com')
    self.assertEqual(patient.email,'johndoe@example.com')

  def test_email_is_unique(self):
    patient1 = Patient(first_name='John',last_name='Doe',email='example@example.com')
    patient2 = Patient(first_name='Jane',last_name='Doe',email='example@example.com')
    
    db.session.add(patient1)
    db.session.commit()

    with self.assertRaises(IntegrityError):
      db.session.add(patient2)
      db.session.commit()

class PatientNoteModelTestCase(FlaskTestCase):
  def test_id(self):
    note = PatientNote(title='title',notes='notes')
    db.session.add(note)
    db.session.commit()
    self.assertEqual(note.id, 1)
    
  def test_repr(self):
    note = PatientNote(title='title',notes='notes')
    self.assertEqual(note.__repr__(), 'title')

  def test_title_and_notes_assignment(self):
    note = PatientNote(title='title',notes='notes')
    self.assertEqual(note.title, 'title')
    self.assertEqual(note.notes, 'notes')
  
  def test_dates_assignment(self):
    before = datetime.utcnow()
    note = PatientNote(title='title',notes='notes')
    db.session.add(note)
    db.session.commit()
    after = datetime.utcnow()
    self.assertTrue(note.date_added > before and note.date_added < after)
    self.assertTrue(note.date_modified > before and note.date_modified < after)

class AppointmentModelTestCase(FlaskTestCase):
  def test_id(self):
    start = datetime.utcnow()
    end = datetime.utcnow() + timedelta(days=1)
    appointment = Appointment(title='title',description='description',
                  date_start=start, date_end = end)
    db.session.add(appointment)
    db.session.commit()
    self.assertEqual(appointment.id, 1)
    
  def test_repr(self):
    start = datetime.utcnow()
    end = datetime.utcnow() + timedelta(days=1)
    appointment = Appointment(title='title',description='description',
                  date_start=start, date_end = end)
    self.assertEqual(appointment.__repr__(), 'title')

  def test_attributes_assignment(self):
    start = datetime.utcnow()
    end = datetime.utcnow() + timedelta(days=1)
    appointment = Appointment(title='title',description='description',
                  date_start=start, date_end = end)
    appointment.color = 'blue'
    appointment.is_completed = True
    self.assertEqual(appointment.title, 'title')
    self.assertEqual(appointment.description, 'description')
    self.assertEqual(appointment.date_start, start)
    self.assertEqual(appointment.date_end, end)
    self.assertEqual(appointment.color, 'blue')
    self.assertEqual(appointment.is_completed, True)

class HospitalModelTestCase(FlaskTestCase):
  def test_id(self):
    hospital = Hospital(name='Severance')
    db.session.add(hospital)
    db.session.commit()
    self.assertEqual(hospital.id, 1)
    
  def test_repr(self):
    hospital = Hospital(name='Severance')
    self.assertEqual(hospital.__repr__(), '<Hospital Severance>')

  def test_attributes_assignment(self):
    hospital = Hospital(name='Severance')
    self.assertEqual(hospital.name, 'Severance')

  def test_get_patients(self):
    hospital = Hospital(name='Severance')
    user = User(first_name='one',last_name='one',email='one@one.com',username='one',password='one')
    patient1 = Patient(first_name='patient',last_name='1',email='patient1@gmail.com')
    patient2 = Patient(first_name='patient',last_name='2',email='patient2@gmail.com')
    patient3 = Patient(first_name='patient',last_name='3',email='patient3@gmail.com')
    patient1.users.append(user)
    patient2.users.append(user)
    user.hospital = hospital
    db.session.add_all([hospital,user,patient1,patient2,patient3])
    db.session.commit()
    self.assertTrue(patient1 in hospital.get_patients().all())
    self.assertTrue(patient2 in hospital.get_patients().all())
    self.assertFalse(patient3 in hospital.get_patients().all())

  def test_get_appointments(self):
    hospital = Hospital(name='Severance')
    user = User(first_name='one',last_name='one',email='one@one.com',username='one',password='one')
    start = datetime.utcnow()
    end = datetime.utcnow() + timedelta(days=1)
    appointment1 = Appointment(title='title',description='description',
                  date_start=start, date_end = end)
    appointment2 = Appointment(title='title',description='description',
                  date_start=start, date_end = end)
    appointment3 = Appointment(title='title',description='description',
                  date_start=start, date_end = end)

    appointment1.user = user
    appointment2.user = user
    user.hospital = hospital
    db.session.add_all([hospital,user,appointment1,appointment2,appointment3])
    db.session.commit()
    self.assertTrue(appointment1 in hospital.get_appointments().all())
    self.assertTrue(appointment2 in hospital.get_appointments().all())
    self.assertFalse(appointment3 in hospital.get_appointments().all())

class UserModelTestCase(FlaskTestCase):
  def test_id(self):
    user = User(first_name='one',last_name='two',email='one@two.com',username='username',password='one')
    db.session.add(user)
    db.session.commit()
    self.assertEqual(user.id,1)
  
  def test_attributes_assignment(self):
    user = User(first_name='one',last_name='two',username='username',email='one@two.com',password='one')
    self.assertEqual(user.first_name,'one')
    self.assertEqual(user.last_name,'two')
    self.assertEqual(user.email,'one@two.com')

  def test_email_is_unique(self):
    user1 = User(first_name='John',last_name='Doe',username='username',email='example@example.com',password='one')
    user2 = User(first_name='Jane',last_name='Doe',username='username',email='example@example.com',password='one')
    
    db.session.add(user1)
    db.session.commit()

    with self.assertRaises(IntegrityError):
      db.session.add(user2)
      db.session.commit()

  def test_repr(self):
    user1 = User(first_name='John',last_name='Doe',username='username',email='example@example.com',password='one')
    self.assertEqual(user1.__repr__(),'<User example@example.com>')

  def test_password_setter(self):
    u = User(first_name='John',last_name='Doe',username='username',email='example@example.com',password='one')
    self.assertTrue(u.password_hash is not None)
  
  def test_no_password_getter(self):
    u = User(first_name='John',last_name='Doe',username='username',email='example@example.com',password='one')
    with self.assertRaises(AttributeError):
      u.password
  
  def test_password_verification(self):
    u = User(first_name='John',last_name='Doe',username='username',email='example@example.com',password='one')
    self.assertTrue(u.verify_password('one'))
    self.assertFalse(u.verify_password('two'))

  def test_password_salts_are_random(self):
    u1 = User(first_name='John',last_name='Doe',username='username',email='example@example.com',password='one')
    u2 = User(first_name='John',last_name='Doe',username='username',email='example@example.com',password='one')
    self.assertTrue(u1.password_hash != u2.password_hash)

class ModelRelationshipsTestCase(FlaskTestCase):
  def test_patient_notes_relationship(self):
    patient = Patient(first_name='John',last_name='Elliot',email="john@elliot.com")
    user = User(first_name='John',last_name='Elliot',username='username',email="john@elliot.com",password='one')  
    patient_note1 = PatientNote(title='title1',notes='note1')
    patient_note2 = PatientNote(title='title2',notes='note2')

    # before connecting
    self.assertEqual(len(patient.patient_notes.all()), 0)
    self.assertEqual(len(user.patient_notes.all()), 0)

    # after connecting patient_note1
    patient_note1.patient = patient
    patient_note1.user = user

    db.session.add_all([patient,user,patient_note1,patient_note2])
    db.session.commit()
    self.assertEqual(len(patient.patient_notes.all()), 1)
    self.assertTrue(patient_note1 in patient.patient_notes.all())
    self.assertEqual(patient_note1.patient_id, patient.id)
    self.assertFalse(patient_note2 in patient.patient_notes.all())
    self.assertNotEqual(patient_note2.patient_id, patient.id)
    self.assertEqual(len(user.patient_notes.all()), 1)
    self.assertTrue(patient_note1 in user.patient_notes.all())
    self.assertEqual(patient_note1.user_id, user.id)
    self.assertFalse(patient_note2 in user.patient_notes.all())
    self.assertNotEqual(patient_note2.user_id, user.id)

  def test_appointments_relationship(self):
    start = datetime.utcnow()
    end = datetime.utcnow() + timedelta(days=1)
    appointment1 = Appointment(title='title1',description='description1',
                  date_start=start, date_end = end)
    appointment2 = Appointment(title='title2',description='description2',
                  date_start=start, date_end = end)
    patient = Patient(first_name='John',last_name='Elliot',email="john@elliot.com")
    user = User(first_name='John',last_name='Elliot',username='username',email="john@elliot.com",password='one')  
    treatment = Treatment(name='Tylenol')

    # before connecting
    self.assertEqual(len(patient.appointments.all()), 0)
    self.assertEqual(len(user.appointments.all()), 0)
    self.assertEqual(len(treatment.appointments.all()), 0)

    # after connecting appointment1
    appointment1.patient = patient
    appointment1.user = user
    appointment1.treatment = treatment

    db.session.add_all([patient,user,treatment,appointment1,appointment2])
    db.session.commit()

    self.assertEqual(len(patient.appointments.all()), 1)
    self.assertTrue(appointment1 in patient.appointments.all())
    self.assertEqual(appointment1.patient_id, patient.id)
    self.assertFalse(appointment2 in patient.appointments.all())
    self.assertNotEqual(appointment2.patient_id, patient.id)    

    self.assertEqual(len(user.appointments.all()), 1)
    self.assertTrue(appointment1 in user.appointments.all())
    self.assertEqual(appointment1.user_id, user.id)
    self.assertFalse(appointment2 in user.appointments.all())
    self.assertNotEqual(appointment2.user_id, user.id)    

    self.assertEqual(len(treatment.appointments.all()), 1)
    self.assertTrue(appointment1 in treatment.appointments.all())
    self.assertEqual(appointment1.treatment_id, treatment.id)
    self.assertFalse(appointment2 in treatment.appointments.all())
    self.assertNotEqual(appointment2.treatment_id, treatment.id)    

  def test_hospital_user_relationship(self):
    user1 = User(first_name='John1',last_name='Elliot1',username='username1',email="john@elliot1.com",password='one1')  
    user2 = User(first_name='John2',last_name='Elliot2',username='username2',email="john@elliot2.com",password='one2')
    hospital = Hospital(name='Severance')

    # before connecting
    self.assertEqual(len(hospital.users.all()),0)

    # after connecting
    user1.hospital = hospital
    user2.hospital = hospital
    self.assertEqual(len(hospital.users.all()),2)
    self.assertEqual(user1.hospital, hospital)
    self.assertEqual(user2.hospital, hospital)
    self.assertTrue(user1 in hospital.users.all())
    self.assertTrue(user2 in hospital.users.all())

  def test_user_patient_relationship(self):
    patient1 = Patient(first_name='one',last_name='one',email='one')
    patient2 = Patient(first_name='two',last_name='two',email='two')
    user1 = User(first_name='three',last_name='three',username='username',email='three',password='one')
    user2 = User(first_name='four',last_name='four',username='username',email='four',password='one')

    # before connecting
    self.assertEqual(len(patient1.users.all()),0)
    self.assertEqual(len(patient2.users.all()),0)
    self.assertEqual(len(user1.patients.all()),0)
    self.assertEqual(len(user2.patients.all()),0)

    # connect patients to user1
    user1.patients.append(patient1)
    user1.patients.append(patient2)
    self.assertEqual(len(user1.patients.all()),2)
    self.assertTrue(patient1 in user1.patients.all())
    self.assertTrue(patient2 in user1.patients.all())
    self.assertFalse(patient1 in user2.patients.all())
    self.assertFalse(patient2 in user2.patients.all())
    self.assertTrue(user1 in patient1.users.all())
    self.assertTrue(user1 in patient2.users.all())

    #undo
    user1.patients.remove(patient1)
    user1.patients.remove(patient2)

    # connect users to patient1
    patient1.users.append(user1)
    patient1.users.append(user2)
    self.assertEqual(len(patient1.users.all()),2)
    self.assertTrue(user1 in patient1.users.all())
    self.assertTrue(user2 in patient1.users.all())
    self.assertFalse(user1 in patient2.users.all())
    self.assertFalse(user2 in patient2.users.all())
    self.assertTrue(patient1 in user1.patients.all())
    self.assertTrue(patient1 in user2.patients.all())
    self.assertFalse(patient2 in user1.patients.all())
    self.assertFalse(patient2 in user2.patients.all())
  
  def test_treatment_hospital_relationship(self):
    hospital1 = Hospital('hospital1')
    hospital2 = Hospital('hospital2')
    
    treatment1 = Treatment('treatment1')
    treatment2 = Treatment('treatment2')

    # before connecting
    self.assertEqual(len(hospital1.treatments.all()),0)
    self.assertEqual(len(hospital2.treatments.all()),0)

    # after connecting
    treatment1.hospital = hospital1
    treatment2.hospital = hospital1
    self.assertEqual(len(hospital1.treatments.all()),2)
    self.assertEqual(hospital1,treatment1.hospital)
    self.assertEqual(hospital1,treatment2.hospital)
    self.assertTrue(treatment1 in hospital1.treatments.all())
    self.assertTrue(treatment2 in hospital1.treatments.all())

    self.assertEqual(len(hospital2.treatments.all()),0)
    self.assertNotEqual(hospital2,treatment1.hospital)
    self.assertNotEqual(hospital2,treatment2.hospital)
    self.assertFalse(treatment1 in hospital2.treatments.all())
    self.assertFalse(treatment2 in hospital2.treatments.all())
  
  def test_database_cascade(self):
    # User and PatientNote
    user = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    patient_note = PatientNote(title='title',notes='notes')
    patient_note.user = user
    db.session.add_all([user,patient_note])
    db.session.commit()
    db.session.delete(user)
    db.session.commit()
    self.assertEqual(len(PatientNote.query.all()), 0)

    # User and Appointment
    user = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    today = datetime.utcnow()
    appointment = Appointment(title='title',description='description',date_start=today,date_end=today)
    appointment.user = user
    db.session.add_all([user,appointment])
    db.session.commit()
    db.session.delete(user)
    db.session.commit()
    self.assertEqual(len(Appointment.query.all()), 0)

    # Patient and PatientNote
    patient = Patient(first_name='patient1',last_name='patient1',email='patient1@gmail.com')
    patient_note = PatientNote(title='title',notes='notes')
    patient_note.patient = patient
    db.session.add_all([patient,patient_note])
    db.session.commit()
    db.session.delete(patient)
    db.session.commit()
    self.assertEqual(len(PatientNote.query.all()), 0)

    # Patient and Appointment
    patient = Patient(first_name='patient1',last_name='patient1',email='patient1@gmail.com')
    appointment = Appointment(title='title',description='description',date_start=today,date_end=today)
    appointment.patient = patient
    db.session.add_all([patient,appointment])
    db.session.commit()
    db.session.delete(patient)
    db.session.commit()
    self.assertEqual(len(Appointment.query.all()), 0)

    # Treatment and Appointment
    treatment = Treatment(name='treatment1')
    appointment = Appointment(title='title',description='description',date_start=today,date_end=today)
    appointment.treatment = treatment
    db.session.add_all([treatment,appointment])
    db.session.commit()
    db.session.delete(treatment)
    db.session.commit()
    self.assertEqual(len(Appointment.query.all()), 0)

    # Hospital and User
    user = User(first_name='one',last_name='one',username='one',email='one@one.com',password='one')
    hospital = Hospital(name='hospital')
    user.hospital = hospital
    db.session.add_all([hospital,user])
    db.session.commit()
    db.session.delete(hospital)
    db.session.commit()
    self.assertEqual(len(User.query.all()), 0)

    # Hospital and Treatment
    treatment = Treatment(name='treatment1')
    hospital = Hospital(name='hospital')
    treatment.hospital = hospital
    db.session.add_all([hospital,treatment])
    db.session.commit()
    db.session.delete(hospital)
    db.session.commit()
    self.assertEqual(len(Treatment.query.all()), 0)
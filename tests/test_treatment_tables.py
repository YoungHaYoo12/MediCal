from flask import url_for
from app.models import User, Hospital,Patient,Treatment,TreatmentTable,TreatmentTableEntry
from base_case import FlaskClientTestCase
from app import db,create_app
from datetime import datetime

class TreatmentTablesTestCase(FlaskClientTestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client(use_cookies=True)


    hospital = Hospital(name='Hospital')
    user = User(first_name='userone',last_name='userone',username='userone',email='userone@one.com',password='userone')
    user.hospital = hospital
    patient = Patient('Patient','100','patient100@gmail.com')
    user.patients.append(patient)
    treatment = Treatment(name='Treatment 1')
    treatment.hospital = hospital
    table1 = TreatmentTable(patient=patient,name='Table 1')
    entry1 = TreatmentTableEntry(amount='Entry1Amount',note='Entry1Note',treatment=treatment,treatment_table=table1)
    db.session.add_all([hospital,user,patient,treatment,table1,entry1])
    db.session.commit()

  def test_add_table(self):
    patient1 = Patient.query.get(1)
    self.assertEqual(len(patient1.treatment_tables.all()),1)
    
    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'userone@one.com', 
        'password': 'userone' 
      }
        )
      
      response = self.client.post(url_for('treatment_tables.add_table',patient_id=patient1.id),data={
        'name':'Added Table'
      },follow_redirects=True)
      data = response.get_data(as_text=True)
      self.assertTrue('Treatment Table Successfully Added' in data)
      self.assertEqual(len(patient1.treatment_tables.all()),2)

  def test_edit_table(self):
    table1 = TreatmentTable.query.get(1)
    self.assertEqual(table1.name,'Table 1')

    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'userone@one.com', 
        'password': 'userone' 
      }
        )
      
      response = self.client.post(url_for('treatment_tables.edit_table',treatment_table_id=table1.id),data={
        'name':'Table 1 Edited'
      },follow_redirects=True)
      data = response.get_data(as_text=True)
      self.assertTrue('Treatment Table Successfully Edited' in data)
      self.assertEqual(table1.name,'Table 1 Edited')

  def test_delete_table(self):
    table1 = TreatmentTable.query.get(1)
    self.assertEqual(len(TreatmentTable.query.all()),1)

    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'userone@one.com', 
        'password': 'userone' 
      }
        )
      
      response = self.client.get(url_for('treatment_tables.delete_table',treatment_table_id=table1.id),follow_redirects=True)
      data = response.get_data(as_text=True)
      self.assertTrue('Treatment Table Successfully Deleted' in data)
      self.assertEqual(len(TreatmentTable.query.all()),0)

  def test_delete_entry(self):
    entry1 = TreatmentTableEntry.query.get(1)
    self.assertEqual(len(TreatmentTableEntry.query.all()),1)

    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'userone@one.com', 
        'password': 'userone' 
      }
        )
      
      response = self.client.get(url_for('treatment_tables.delete_entry',treatment_entry_id=entry1.id),follow_redirects=True)
      data = response.get_data(as_text=True)
      self.assertTrue('Entry Successfully Deleted' in data)
      self.assertEqual(len(TreatmentTableEntry.query.all()),0)

  def test_list(self):
    patient1 = Patient.query.get(1)
    
    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'userone@one.com', 
        'password': 'userone' 
      }
        )
      response = self.client.get(url_for('treatment_tables.list',patient_id=patient1.id))
      data = response.get_data(as_text=True)
      self.assertTrue('Table 1' in data)

  def test_table(self):
    treatment = Treatment.query.get(1)
    table1 = TreatmentTable.query.get(1)

    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'userone@one.com', 
        'password': 'userone' 
      }
          )
      response = self.client.get(url_for('treatment_tables.table',treatment_table_id=table1.id))
      data = response.get_data(as_text=True)
      self.assertTrue('Entry1Amount' in data)
      self.assertTrue('Entry1Note' in data)

      # post form data to add new entry 
      date = datetime.utcnow()
      response = self.client.post(url_for('treatment_tables.table',treatment_table_id=table1.id),data={
        'treatment':treatment.id,
        'date':date,
        'amount':'Entry2Amount',
        'note':'Entry2Note'
      },follow_redirects=True)
      data = response.get_data(as_text=True)
      self.assertTrue('Entry2Amount' in data)
      self.assertTrue('Entry2Note' in data)

  def test_invalid_url_parameters(self):
    patient2 = Patient('Patient','200','patient200@gmail.com')
    table2 = TreatmentTable(patient=patient2,name='Table 2')
    entry2 = TreatmentTableEntry(amount='Amount',note='Note',treatment_table=table2)
    db.session.add_all([patient2,table2,entry2])
    db.session.commit()
    with self.client:
      self.client.post(url_for('auth.login'), data=
      { 
        'email': 'userone@one.com', 
        'password': 'userone' 
      }
        )
      # list
      response = self.client.get(url_for('treatment_tables.list',patient_id=100))
      self.assertEqual(response.status_code,404)
      response = self.client.get(url_for('treatment_tables.list',patient_id=2))
      self.assertEqual(response.status_code,403)

      # table
      response = self.client.get(url_for('treatment_tables.table',treatment_table_id=100))
      self.assertEqual(response.status_code,404)
      response = self.client.get(url_for('treatment_tables.table',treatment_table_id=table2.id))
      self.assertEqual(response.status_code,403)

      # add_table 
      response = self.client.get(url_for('treatment_tables.add_table',patient_id=100))
      self.assertEqual(response.status_code,404)
      response = self.client.get(url_for('treatment_tables.add_table',patient_id=patient2.id))
      self.assertEqual(response.status_code,403)

      # edit_table
      response = self.client.get(url_for('treatment_tables.edit_table',treatment_table_id=100))
      self.assertEqual(response.status_code,404)
      response = self.client.get(url_for('treatment_tables.edit_table',treatment_table_id=table2.id))
      self.assertEqual(response.status_code,403)

      # delete_table
      response = self.client.get(url_for('treatment_tables.delete_table',treatment_table_id=100))
      self.assertEqual(response.status_code,404)
      response = self.client.get(url_for('treatment_tables.delete_table',treatment_table_id=table2.id))
      self.assertEqual(response.status_code,403)

      # delete_entry 
      response = self.client.get(url_for('treatment_tables.delete_entry',treatment_entry_id=100))
      self.assertEqual(response.status_code,404)
      response = self.client.get(url_for('treatment_tables.delete_entry',treatment_entry_id=entry2.id))
      self.assertEqual(response.status_code,403)
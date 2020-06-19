from flask import render_template, redirect, url_for, flash,request
from flask_login import login_required, current_user
from app import db
from app.treatments import treatments
from app.treatments.forms import TreatmentForm
from app.models import Treatment

@treatments.route('/list')
@login_required
def list():
  page = request.args.get('page',1,type=int)

  pagination = current_user.hospital.treatments.order_by(Treatment.name).paginate(page=page,per_page=20)

  treatments = pagination.items

  return render_template('treatments/list.html', pagination=pagination,treatments=treatments)

@treatments.route('/add', methods=['GET','POST'])
@login_required
def add():
  form = TreatmentForm()

  if form.validate_on_submit():
    hospital = current_user.hospital

    # create new treatment if it does not already exist
    treatment = Treatment.query.filter_by(name=form.name.data).first()
    if treatment is None:
      treatment = Treatment(name=form.name.data)
    
    # if hospital already has treatment, redirect
    if hospital in treatment.hospitals.all():
      flash('Hospital Already Has Treatment')
      return redirect(url_for('treatments.list'))

    # add treatment to hospital
    treatment.hospitals.append(hospital)

    db.session.add(treatment)
    db.session.commit()
    flash('Treatment Successfully Added')
    return redirect(url_for('treatments.list'))
  
  return render_template('treatments/add.html',form=form)
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db
from app.auth import auth
from app.models import User,Hospital
from app.auth.forms import LoginForm, RegistrationForm

@auth.route('/register',methods=['GET','POST'])
def register():
  form = RegistrationForm()

  # form processing
  hospitals_tuple = []
  hospitals = Hospital.query.order_by(Hospital.name.asc()).all()
  for hospital in hospitals:
    hospitals_tuple.append((hospital.name,hospital.name))
  form.hospital.choices = hospitals_tuple

  if form.validate_on_submit():
      # temporarily block off registration
    flash('Registering Currently Not Available')
    return redirect(url_for('auth.login'))

    # create user
    u = User(first_name=form.first_name.data,
                  last_name=form.last_name.data,
                  username=form.username.data,
                  email=form.email.data,
                  password=form.password.data)

    # connect user to hospital
    hospital = Hospital.query.filter_by(name=form.hospital.data).first_or_404()
    u.hospital = hospital

    db.session.add(u)
    db.session.commit()

    flash('Successfully Registered')
    return redirect(url_for('auth.login'))

  return render_template('auth/register.html',form=form)

@auth.route('/login', methods=['GET','POST'])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    u = User.query.filter_by(email=form.email.data).first()
    if u is not None and u.verify_password(form.password.data):
      flash('Logged In Successfully')
      login_user(u,form.remember_me.data)
      next = request.args.get('next')
      if next == None or not next[0] == '/':
        next = url_for('core.index')
      return redirect(next)

    flash('Invalid Username or Password')

  return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Successfully Logged Out')
  return redirect(url_for('core.index'))

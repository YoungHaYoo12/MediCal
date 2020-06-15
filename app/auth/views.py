from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db
from app.auth import auth
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm

@auth.route('/register',methods=['GET','POST'])
def register():
  form = RegistrationForm()

  if form.validate_on_submit():
    u = User(first_name=form.first_name.data,
                  last_name=form.last_name.data,
                  username=form.username.data,
                  email=form.email.data,
                  password=form.password.data)
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
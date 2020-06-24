from datetime import datetime
from flask import render_template, session, redirect, url_for, request,abort
from flask_login import login_required, current_user
from app.calendars.functions import get_next_seven_days, get_next_thirty_days
from app.core import core
from app.core.forms import UserSearchForm
from app.appointments.views import get_month_appointments_dict, get_week_appointments_dict, get_day_appointments_dict,remove_duplicate_appointments
from app.models import User

@core.route('/')
def index():
  return render_template('core/index.html')

@core.route('/search/users',methods=['GET','POST'])
@login_required
def search_users():
  page = request.args.get('page',1,type=int)
  # form processing
  form = UserSearchForm()

  if form.validate_on_submit():
    session['username'] = form.username.data
    session['first_name'] = form.first_name.data
    session['last_name'] = form.last_name.data

    return redirect(url_for('core.search_users'))
  
  elif request.method == 'GET':
    if session.get('username') is not None:
      form.username.data = session.get('username')
    if session.get('first_name') is not None:
      form.first_name.data = session.get('first_name')
    if session.get('last_name') is not None:
      form.last_name.data = session.get('last_name')    

  # get list of users that satisfy search query
  query = current_user.hospital.users
  if session.get('username') is not None and len(session.get('username'))!=0:
    query = query.filter_by(username = session.get('username'))
  if session.get('first_name') is not None and len(session.get('first_name'))!=0:
    query = query.filter_by(first_name = session.get('first_name'))
  if session.get('last_name') is not None and len(session.get('last_name'))!=0:
    query = query.filter_by(last_name = session.get('last_name'))

  pagination = query.paginate(page=page,per_page=12)
  users = pagination.items

  return render_template('core/search_users.html',form=form,pagination=pagination,users=users,username=session.get('username'),first_name=session.get('first_name'),last_name=session.get('last_name'))

@core.route('/user/<username>')
@login_required
def user(username):
  user = User.query.filter_by(username=username).first_or_404()

  # validate user 
  if user.hospital != current_user.hospital:
    abort(403)
  
  # retrieve upcoming appointments
  # today
  today = datetime.utcnow()
  today_appointments_complete = get_day_appointments_dict(day=today,user=user,is_completed=True)
  today_appointments_incomplete = get_day_appointments_dict(day=today,user=user,is_completed=False)

  # next 7 days 
  seven_days = get_next_seven_days(today.year,today.month,today.day)
  seven_days_appointments_complete = get_week_appointments_dict(week=seven_days,user=user,is_completed=True)
  seven_days_appointments_incomplete = get_week_appointments_dict(week=seven_days,user=user,is_completed=False)
  remove_duplicate_appointments(seven_days_appointments_complete)
  remove_duplicate_appointments(seven_days_appointments_incomplete)

  # next 30 days
  thirty_days = get_next_thirty_days(today.year,today.month,today.day)
  thirty_days_appointments_complete = get_week_appointments_dict(week=thirty_days,user=user,is_completed=True)
  thirty_days_appointments_incomplete = get_week_appointments_dict(week=thirty_days,user=user,is_completed=False)
  remove_duplicate_appointments(thirty_days_appointments_complete)
  remove_duplicate_appointments(thirty_days_appointments_incomplete)

  return render_template('core/user.html',user=user,
                          today=today,
                          seven_days=seven_days,
                          thirty_days=thirty_days,  today_appointments_complete=today_appointments_complete,today_appointments_incomplete=today_appointments_incomplete,seven_days_appointments_complete=seven_days_appointments_complete,seven_days_appointments_incomplete=seven_days_appointments_incomplete,thirty_days_appointments_complete=thirty_days_appointments_complete,thirty_days_appointments_incomplete=thirty_days_appointments_incomplete,patients=user.patients.all())
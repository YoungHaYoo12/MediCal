from flask import render_template, session, redirect, url_for, request,abort,make_response
from flask_login import login_required, current_user
from app.core import core
from app.core.forms import UserSearchForm
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

  return render_template('core/user.html',user=user,patients=user.patients.all())
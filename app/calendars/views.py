from flask import render_template, request, jsonify
from calendar import Calendar
import datetime
from app.calendars import calendars

cal = Calendar(7)

@calendars.route('/month/<int:year>/<int:month>')
def month(year,month):
  weeks = get_weeks(year,month)
  return render_template('calendars/month.html',weeks=weeks)

@calendars.route('/week/<int:year>/<int:month>/<int:week>')
def week(year,month,week):
  weeks = get_weeks(year,month)
  return render_template('calendars/week.html',week=weeks[week])

@calendars.route('/create/event',methods=['POST'])
def create_event():
  date_str = request.form['date']
  year = int(date_str[0:4])
  month = int(date_str[5:7])
  day = int(date_str[8:])
  date = datetime.date(year,month,day)
  print(date)


  return jsonify({
    'result':'success'
  })

####### HELPER FUNCTIONS #######
def get_weeks(year,month):
  month_days = []
  for day in cal.itermonthdates(int(year),month):
    month_days.append(day)
  weeks = [
    month_days[0:7],
    month_days[7:14],
    month_days[14:21],
    month_days[21:28],
    month_days[28:35]
  ]
  return weeks
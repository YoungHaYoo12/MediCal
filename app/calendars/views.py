from flask import render_template
from calendar import Calendar
from app.calendars import calendars

cal = Calendar(7)

@calendars.route('/month/<int:year>/<int:month>')
def month(year,month):
  weeks = get_weeks(year,month)
  return render_template('calendars/month.html',weeks=weeks)

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
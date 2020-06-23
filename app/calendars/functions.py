from calendar import Calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta

cal = Calendar(6)

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

def get_next_seven_days(year,month,day):
  current_day = datetime(year,month,day)
  return [current_day,
          current_day+relativedelta(days=1),
          current_day+relativedelta(days=2),
          current_day+relativedelta(days=3),
          current_day+relativedelta(days=4),
          current_day+relativedelta(days=5),
          current_day+relativedelta(days=6)
          ]

def get_next_thirty_days(year,month,day):
  current_day = datetime(year,month,day)
  next_thirty_days = []
  for i in range(30):
    next_thirty_days.append(current_day+relativedelta(days=i))
  return next_thirty_days

def validate_year(year):
  return year >= 2 and year <= 9998

def validate_date(year,month,day):
  try:
    datetime(year,month,day)
  except ValueError:
    return False
  
  return True
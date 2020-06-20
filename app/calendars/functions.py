from calendar import Calendar

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

def validate_year(year):
  return year >= 2 and year <= 9998

def validate_month(month):
  return month <= 12 and month >= 1
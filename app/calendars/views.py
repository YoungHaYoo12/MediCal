from app.calendars import calendars

@calendars.route('/')
def calendar():
  return 'Calendar Page'
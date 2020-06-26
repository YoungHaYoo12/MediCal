# Unit Test functions in calendars
import unittest
from app.calendars.functions import get_weeks, validate_year, validate_date, get_next_seven_days, get_next_thirty_days
from datetime import datetime
from dateutil.relativedelta import relativedelta

class CalendarsTestCase(unittest.TestCase):
  def test_validate_year(self):
    # out of bounds
    self.assertFalse(validate_year(1))
    self.assertFalse(validate_year(9999))

    # at boundaries 
    self.assertTrue(validate_year(2))
    self.assertTrue(validate_year(9998))

    # within bounds
    self.assertTrue(validate_year(2020))
    self.assertTrue(validate_year(5951))

  def test_get_weeks(self):
    # February 2020 weeks
    weeks = get_weeks(2020,2)
    self.assertEqual(len(weeks),5)
    for week in weeks:
      self.assertEqual(len(week),7)
    
    first_day = weeks[0][0]
    self.assertEqual(first_day.year,2020)
    self.assertEqual(first_day.month,1)
    self.assertEqual(first_day.day,26)
    
    last_day = weeks[4][6]
    self.assertEqual(last_day.year,2020)
    self.assertEqual(last_day.month,2)
    self.assertEqual(last_day.day,29)
  
  def test_validate_date(self):
    # Test errors in year 
    self.assertFalse(validate_date(0,1,1))
    self.assertFalse(validate_date(10000,1,1))

    # Test Errors in month
    self.assertFalse(validate_date(2020,0,1))
    self.assertFalse(validate_date(2020,13,1))

    # Test Errors in day
    self.assertFalse(validate_date(2020,1,0))
    self.assertFalse(validate_date(2020,1,32))

    # Test Successful 
    self.assertTrue(validate_date(2020,6,26))

    # Test Lunar New Year
    self.assertTrue(validate_date(2020,2,29))
    self.assertFalse(validate_date(2021,2,29))

  def test_get_next_seven_days(self):
    current_day = datetime(2020,6,20)
    seven_days = get_next_seven_days(2020,6,20)
    for i in range(7):
      self.assertTrue(seven_days[i] == current_day + relativedelta(days=i))

  def test_get_next_thirty_days(self):
    current_day = datetime(2020,6,20)
    thirty_days = get_next_thirty_days(2020,6,20)
    for i in range(30):
      self.assertTrue(thirty_days[i] == current_day + relativedelta(days=i))
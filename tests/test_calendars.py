# Unit Test functions in calendars
import unittest
from app.calendars.functions import get_weeks, validate_year, validate_month

class CalendarsTestCase(unittest.TestCase):
  def test_validate_month(self):
    # out of bounds
    self.assertFalse(validate_month(0))
    self.assertFalse(validate_month(13))

    # at boundaries 
    self.assertTrue(validate_month(1))
    self.assertTrue(validate_month(12))

    # within bounds
    self.assertTrue(validate_month(7))
    self.assertTrue(validate_month(9))
  
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
# Unit Test functions in calendars
import unittest
from app.calendars.functions import get_weeks, validate_year

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
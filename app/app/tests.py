""" 
Sample tests
""" # noqa 
from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    """ Test the calc module """

    def test_add_numbers(self):
        """ Test sum calc """
        res = calc.add(5, 6)
        self.assertEqual(res, 11)

    def test_subtract_numbers(self):
        """ Test subtsracting number """
        res = calc.subtract(10, 15)
        self.assertEqual(res, 5)

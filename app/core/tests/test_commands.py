"""
    Test custom Django management command
    # https://stackoverflow.com/questions/75042748/django-project-wait-for-database-ready-tests
"""
""" mock behavior of database """
from unittest.mock import patch # noqa
""" OperationalError is one of possiblility error we may get,
when we try to connect db, be4 db is ready """
from psycopg2 import OperationalError as Psycopg2Error # noqa

from django.core.management import call_command # noqa
""" OperationalError another exception that may get through by the db,
depending what state of the start of process """
from django.db.utils import OperationalError # noqa
""" Base test use for unit test. We're testing the db if avaiable. """
from django.test import SimpleTestCase # noqa


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """ Test command """
    def test_wait_for_db_ready(self, patched_check):
        """ Test waiting for db if db ready. """
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """ Test waiting for db when getting OperationalError """
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])

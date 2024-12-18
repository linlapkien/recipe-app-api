"""
Django command to wait for the database to be available
# https://stackoverflow.com/questions/75042748/django-project-wait-for-database-ready-tests
"""
import time # noqa

from psycopg2 import OperationalError as Psycopg20pError # noqa

""" Error Django throws when db is not ready """
from django.db.utils import OperationalError # noqa
from django.core.management.base import BaseCommand # noqa


class Command(BaseCommand):
    """ Django command to wait for db """

    def handle(self, *args, **options):
        """  Entrypoint for command """
        """ stdout.write log a mess to a screen """
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg20pError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available!"))

from django.core.management.base import BaseCommand
from django.db import transaction

from scripts.populate_db import DataPopulate


class Command(BaseCommand):
    help = 'Populate database with fake data'

    def handle(self, *args, **kwargs):
        populate_db = DataPopulate()

        try:
            with transaction.atomic():
                populate_db.populate()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {e}'))
            raise e
        else:
            self.stdout.write(self.style.SUCCESS('Database populated with fake data!'))

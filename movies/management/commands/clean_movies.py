from django.core.management.base import BaseCommand

from scripts.movie import DataCleaner


class Command(BaseCommand):
    help = 'Clean movies by deleting all data in blog app'

    def handle(self, *args, **options):
        cleaner = DataCleaner()
        cleaner.clean()
        self.stdout.write(self.style.SUCCESS('Movies cleaned!'))

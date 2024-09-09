from django.core.management.base import BaseCommand

from scripts.blog.clean import DataCleaner


class Command(BaseCommand):
    help = 'Clean database by deleting all data in blog app'

    def handle(self, *args, **options):
        cleaner = DataCleaner()
        cleaner.clean()
        self.stdout.write(self.style.SUCCESS('Database cleaned!'))

import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
application = get_wsgi_application()

with open('dump_json/data.json', mode='w', encoding='utf-8') as file:
    call_command('dumpdata', 'accounts', 'api', 'blog', 'movies', indent=4, stdout=file)

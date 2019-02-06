import os
import re
import sys
from pkg_resources import load_entry_point
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Run celery worker'

    def handle(self, *args, **kwargs):
        sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
        sys.exit(
            load_entry_point('flower==0.9.2', 'console_scripts', 'flower')()
        )








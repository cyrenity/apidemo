import re
import sys
from pkg_resources import load_entry_point
from django.core.management.base import BaseCommand
from django.utils import autoreload


class Command(BaseCommand):
    help = 'Run Flow-er'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-n', '--natural-time', type=str, help='Comma seperated list of queues e.g. -Q default,feed_tasks')

    def handle(self, *args, **kwargs):
        autoreload.main(self._restart_flower())

    @classmethod
    def _restart_flower(self):
        sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
        sys.exit(
            load_entry_point('flower==0.9.2', 'console_scripts', 'flower')()
        )

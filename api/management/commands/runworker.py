from __future__ import absolute_import, unicode_literals
from django.core.management.base import BaseCommand
from config.celery import app
from django.utils import autoreload
from django.utils.autoreload import run_with_reloader



class Command(BaseCommand):
    help = 'Run celery worker'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-Q', '--queues', type=str, help='Comma seperated list of queues e.g. -Q default,feed_tasks')

    def handle(self, *args, **kwargs):
        self.__setattr__('queues', kwargs['queues'])
        run_with_reloader(self._restart_celery)

    def _restart_celery(self):

        if not self.queues:
            self.queues = 'default'

        argv = [
            'worker',
            '--loglevel=INFO',
            '-Q%s' % (self.queues.strip())
        ]

        app.worker_main(argv)

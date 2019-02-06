from __future__ import absolute_import, unicode_literals
import os
from django.core.management.base import BaseCommand
from proj.celery import  app

class Command(BaseCommand):
    help = 'Run celery worker'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-Q', '--queues', type=str, help='Comma seperated list of queues e.g. -Q default,feed_tasks')

    def handle(self, *args, **kwargs):
        queues = kwargs['queues']

        if not queues:
            queues = 'default'

        argv = [
            'worker',
            '--loglevel=INFO',
            '-Q %s' % queues
        ]
        app.worker_main(argv)

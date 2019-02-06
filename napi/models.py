from django.db import models, connection
from django.db.models.fields import *


TYPES = [('type1', 'Type 1'), ('type2', 'Type 2'), ('type3', 'Type 3')]
GENDER = [('male', 'Male'), ('female', 'Female'), ('trans', 'Transgender/Other')]


def sequence_id():
  with connection.cursor() as cursor:
    cursor.execute("""SELECT nextval('tracking_id_seq')""")
    return cursor.fetchone()[0]


class ProcessQueueAction(models.Model):
    tracking_id = BigIntegerField(primary_key=True, default=sequence_id)
    name = CharField(max_length=40)
    phone = BigIntegerField()
    gender = CharField(max_length=10, choices=GENDER)
    type = CharField(max_length=10, choices=TYPES)
    remarks = TextField(max_length=100)
    citizen_number = CharField(max_length=15)
    created = DateTimeField(auto_now=True)
    owner = CharField(max_length=40)


class Tasks(models.Model):
    name = CharField(max_length=40)
    task_id = CharField(max_length=100)
    tracking = models.ForeignKey(ProcessQueueAction, on_delete=models.CASCADE, related_name='tasks')

    def __unicode__(self):
        return '%d: %s' % (self.task_id, self.name)

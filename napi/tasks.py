from proj.celery import app
from celery.signals import task_failure
import time


class VerificationTask(app.Task):
    queue = 'default'
    name = "{}.verification".format(__name__)
    track_started = True

    def run(self, data):
        time.sleep(5)
        data = {'result': "Verification process completed successfully"}
        return data


class ReadyForNumberTask(app.Task):
    queue = 'default'
    name = "{}.ready_for_number".format(__name__)
    track_started = True

    def run(self, data):
        time.sleep(10)
        data = {'number': '1234-999-111', 'result': "Number allocated"}
        return data


class PreparationTask(app.Task):
    queue = 'default'
    name = "{}.preparation".format(__name__)
    track_started = True
    retries = 5
    default_retry_delay = 10

    def run(self, data, args):
        time.sleep(10)
        try:
            data = {'result': "Preparation process completed successfully"}
            return data
        except:
            self.retry()


class PrintingTask(app.Task):
    queue = 'default'
    name = "{}.printing".format(__name__)
    track_started = True

    def run(self, data):
        self.update_state(state="PRINTING", meta={'info': 'Printing is in process'})
        time.sleep(10)
        data = {'result': "Printed"}
        return data


class PersonalizationTask(app.Task):
    queue = 'default'
    name = "{}.personalization".format(__name__)
    track_started = True

    def run(self, data):
        time.sleep(5)
        data = {'result': "Card is successfully personalized"}
        return data


@task_failure.connect()
def failure_handler(sender=None, exception=None, traceback=None, args=None, einfo=None, **kwargs):
    print("ON FAILURE caught: task_name: {0} task_id: {1} message: {2}".format(sender.name, sender.request.id, exception))


app.tasks.register(VerificationTask)
app.tasks.register(ReadyForNumberTask)
app.tasks.register(PreparationTask)
app.tasks.register(PrintingTask)
app.tasks.register(PersonalizationTask)

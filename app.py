# -*- coding: utf-8 -*-

import random
import time

from flask import Flask
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

task_id = None

@app.route('/mount/<string:id>', methods=['GET'])
def mount(id):
    """
    API handler receives /mount/<id> REST call. Passes it to a worker to
    mount a drive with <id>. Returns success (1) or fail (0) after mounting
    is complete.
    """
    if mount_id(id):
        return "1", 200
    else:
        return "0", 400


@app.route('/process', methods=['GET'])
def process():
    """
    API handler receives /process REST call. Starts a CPU intensive and long
    process (could be a dummy file copy process). While the process is
    continuing in the background it returns with a return code.
    """
    global task_id
    task = long_process.apply_async()
    if task:
        task_id = task.task_id
        return "1", 200
    else:
        return "0", 400


@app.route('/process-status', methods=['GET'])
def process_status():
    """
    API handler receives /process-status REST call. Returns 1 if the
    previous task is finished, 0 if still continuing.
    """
    if task_id is None:
        return "1", 400

    task = long_process.AsyncResult(task_id)
    if task.state == 'PENDING':
        return "0", 200
    elif task.state != 'FAILURE':
        return "1", 200
    else:
        return "1", 400


def mount_id(id):
    """
    Worker to mount a drive with <id>. Returns success (1) or fail (0) after
    mounting is complete.
    """
    if random.random() < 0.25:
        return 0
    else:
        return 1


@celery.task(bind=True)
def long_process(self):
    """
    Starts a CPU intensive and long process
    """
    delay = random.randint(60, 120)
    print "long_process is busy waiting for %s seconds" % delay

    start = time.time()
    end = start + delay

    # this is a horrible example of busy waiting
    counter = 1
    while end > time.time():
        # just to make sure the loop is not optimized
        counter = counter+1

    print "long_process finished with counter %s" % counter
    return {'current': counter, 'result': 42}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



import os
import sys
from argparse import ArgumentParser

from celery import Celery
from flask import Flask

from tasks import long_task

# app = Flask(__name__)
app = Flask("app")

# Configure Celery (using Redis as broker)
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"

# Initialize Celery
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)


# A simple Celery task
@celery.task
def my_background_task(arg):
    return long_task(task_name=arg)


@app.route("/task_status/<task_id>")
def task_status(task_id):
    task = my_background_task.AsyncResult(task_id)
    if task.state == "PENDING":
        response = {"state": task.state, "status": "Pending..."}
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "result": task.result,
        }
    else:
        # something went wrong in the background job
        response = {
            "state": task.state,
            "status": str(task.info),  # this is the exception raised
        }
    return response


@app.route("/start_task/<arg>")
def start_task(arg):
    task = my_background_task.apply_async(args=[arg])
    return {"task_id": str(task.id)}, 202


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    app.run(debug=True, port=args.port)
    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())

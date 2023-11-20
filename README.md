# Install Dependencies for worker

```shell
python -m pip install flask requests celery redis
```

# Run server and a worker

### 1. Run server
```shell
python app.py
```

This will start a server on port 5000.

### 2. Run a worker

From a different terminal, run the following command to start a worker.
The worker will listen to the celery queue and execute the tasks.

```shell
celery -A app.celery worker --loglevel=info
```

# Client | Make a request

### 1. start a task

```shell
# curl http://127.0.0.1:5000/start_task/<task-name>
curl http://127.0.0.1:5000/start_task/test
```

This will create a task and put it in the celery queue.
It will return a task id.
The task id can be used to query the status of the task and get the result.

The response looks like this:
```json
{
  "task_id": "b1b0b1b0-1b0b-1b0b-1b0b-1b0b1b0b1b0b"
}
```

### 2. Retrieve status and result

The client can then poll the server to get the status of the task and the result when the task is finished.
Use the task id returned from the previous step.

```shell
# curl http://127.0.0.1:5000/task_status/<task-id>
curl http://127.0.0.1:5000/task_status/b1b0b1b0-1b0b-1b0b-1b0b-1b0b1b0b1b0b
```

The response for a pending task looks like this:
```json
{
  "state": "PENDING",
  "status": "Pending..."
}
```

The response for a completed task looks like this:
```json
{
  "result": {
    "message": "task 'test' says 'hello!'"
  },
  "state": "SUCCESS"
}
```

# Flush Redis DB ( useful for development )

```shell
python flush_redis.py
```

### Implementation details

The server uses **Flask** to handle the requests. \
**Flask** is a micro web framework written in Python.

The server uses **Celery** to create tasks and put them in the queue. \
**Celery** is an asynchronous task queue based on distributed message passing.

Celery uses **Redis** as the message broker.
Redis is a fully-fledged in-memory data structure store, used as a database, cache and in this case as a message broker.

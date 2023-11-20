import time


def long_task(task_name: str):
    time.sleep(10)
    return {"message": f"task '{task_name}' says 'hello!'"}

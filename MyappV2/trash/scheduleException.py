"""purpose: i want to restart the thread once it throw an exception
problem: cannot restart thread based on stackoverflow
starus: failed"""

import functools
import schedule

import threading
import time
import schedule

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator

@catch_exceptions(cancel_on_failure=True)
def bad_task():
    print("bad task")
    return 1 / 0

schedule.every(2).seconds.do(run_threaded, bad_task)

while 1:
    schedule.run_pending()
    time.sleep(1)
import time
from typing import Callable

def retry(func: Callable, retries: int = 3, delay_seconds: int = 2):
    last_exception = None

    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            last_exception = e
            time.sleep(delay_seconds)

    raise last_exception

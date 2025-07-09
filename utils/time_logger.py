import time
from functools import wraps
import warnings
warnings.filterwarnings("ignore")

def timeit(module_name=""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            duration = end - start
            print(f"⏱️ [{module_name}] finished in {duration:.2f} seconds.")
            return result
        return wrapper
    return decorator
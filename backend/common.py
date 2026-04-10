from functools import wraps
import time


def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()
        print(f"[TIME] {func.__name__}: {end - start:.6f} sec")

        return result
    return wrapper
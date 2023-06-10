import logging
import time


def cache(delay):
    def retry_decorator(func):
        last_updated = 0
        cached_value = None

        def _wrapper(*args, **kwargs):
            nonlocal last_updated, cached_value

            if "no_cache" in kwargs and kwargs["no_cache"]:
                del kwargs["no_cache"]
                return func(*args, **kwargs)

            if time.time() - last_updated > delay:
                last_updated = time.time()
                cached_value = func(*args, **kwargs)

            return cached_value

        return _wrapper

    return retry_decorator

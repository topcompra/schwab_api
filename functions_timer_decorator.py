# Create a decorator to time the function's runtime
import time
import logging
import asyncio
from functools import wraps

def timeit(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)  # Await the async function
        end_time = time.time()
        runtime = end_time - start_time
        logging.info(f"Async function '{func.__name__}' took {runtime:.3f} seconds to execute.")
        return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)  # Run the sync function
        end_time = time.time()
        runtime = end_time - start_time
        logging.info(f"Sync function '{func.__name__}' took {runtime:.3f} seconds to execute.")
        return result

    # Check if the function is async or sync
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
    

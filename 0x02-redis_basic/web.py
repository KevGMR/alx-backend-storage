#!/usr/bin/env python3
import requests
import time
from functools import wraps
from typing import Dict, Tuple

cache: Dict[str, Tuple[str, float]] = {}  # (cached_result, timestamp)
cache_count: Dict[str, Tuple[int, float]] = {}  # (access_count, last_access_timestamp)


def cache_with_expiration(expiration: int):
    """
    Decorator to cache the result of the get_page function with an expiration time.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            current_time = time.time()

            # Check cache for the result and access count for this URL
            if url in cache:
                cached_result, timestamp = cache[url]
                if current_time - timestamp < expiration:  # Cache is valid
                    print(f"Returning cached page for {url}")
                    _increment_count(url)
                    return cached_result
                else:
                    print(f"Cache expired for {url}")

            # If cache is not valid or doesn't exist, call the function
            result = func(*args, **kwargs)
            cache[url] = (result, current_time)  # Update cache
            _increment_count(url)  # Increment access count
            return result

        return wrapper
    return decorator


@cache_with_expiration(10)
def get_page(url: str) -> str:
    """
    Fetches the page content from the given URL and caches it.
    """
    print(f"Fetching page from the web: {url}")
    response = requests.get(url)
    return response.text


def _increment_count(url: str):
    """
    Helper function to track how many times a URL is accessed.
    """
    current_time = time.time()
    if url in cache_count:
        count, last_access = cache_count[url]
        cache_count[url] = (count + 1, current_time)
    else:
        cache_count[url] = (1, current_time)

    print(f"URL '{url}' accessed {cache_count[url][0]} times.")


# Test the function with a slow URL to simulate the cache behavior
if __name__ == "__main__":
    slow_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"

    # First access should fetch from the web
    page = get_page(slow_url)

    # Second access within 10 seconds should return from cache
    time.sleep(3)
    page = get_page(slow_url)

    # Access after cache expiration (10 seconds)
    time.sleep(11)
    page = get_page(slow_url)

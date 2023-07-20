#!/usr/bin/env python3
"""5. Implementing an expiring web cache and tracker"""

from requests import get
import redis
from functools import wraps
from typing import Callable

import time

# Decorator for caching
def cache_with_expiry(seconds):
    cache = {}

    def decorator(func):
        def wrapper(url):
            if url in cache and time.time() - cache[url]['timestamp'] < seconds:
                print(f"Cache hit for {url}")
                return cache[url]['content']
            else:
                print(f"Cache miss for {url}")
                content = func(url)
                cache[url] = {
                    'content': content,
                    'timestamp': time.time()
                }
                return content
        return wrapper
    return decorator

@cache_with_expiry(seconds=10)
def get_page(url):
    response = requests.get(url)
    return response.text

# Test the function
url_to_fetch = "http://slowwly.robertomurray.co.uk/delay/5000/url/https://example.com"  # Example slow URL
page_content = get_page(url_to_fetch)
print(page_content)

# Test again after 5 seconds to check the caching
time.sleep(5)
page_content_cached = get_page(url_to_fetch)
print(page_content_cached)


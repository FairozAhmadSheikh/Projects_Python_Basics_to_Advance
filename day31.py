import random
import time
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed

# 1. Fibonacci Sequence with Memoization
@lru_cache(maxsize=128)
def fibonacci(n):
    """
    Calculates the nth Fibonacci number using memoization (caching).
    This makes it very efficient for larger numbers.
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
#!/usr/bin/env python3
"""Module providing a Cache
class for Redis operations with method call counting, history, and replay."""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.

    Args:
        method: The method to be decorated.

    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.

    Args:
        method: The method to be decorated.

    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store input arguments
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function
        output = method(self, *args, **kwargs)

        # Store output
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper


def replay(method: Callable):
    """
    Display the history of calls of a particular function.

    Args:
        method: The method to replay.
    """
    redis_instance = redis.Redis()
    method_name = method.__qualname__
    inputs = redis_instance.lrange(f"{method_name}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{method_name}:outputs", 0, -1)
    calls_count = redis_instance.get(method_name).decode("utf-8")

    print(f"{method_name} was called {calls_count} times:")
    for input_args, output in zip(inputs, outputs):
        input_str = input_args.decode("utf-8")
        output_str = output.decode("utf-8")
        print(f"{method_name}(*{input_str}) -> {output_str}")


class Cache:
    """A class for caching data using Redis with method call counting
    and history."""

    def __init__(self):
        """Initialize the Cache with a Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key.

        Args:
            data: The data to be stored. Can be a string, bytes,
            integer, or float.

        Returns:
            str: The randomly generated key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[
                    str, bytes, int, float, None]:
        """
        Retrieve data from Redis for the given key and apply
        optional conversion.

        Args:
            key: The key to retrieve data for.
            fn: Optional callable to convert the retrieved data.

        Returns:
            The retrieved data, optionally converted,
            or None if the key doesn't exist.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve a UTF-8 string from Redis for the given key.

        Args:
            key: The key to retrieve data for.

        Returns:
            The retrieved string, or None if the key doesn't exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve an integer from Redis for the given key.

        Args:
            key: The key to retrieve data for.

        Returns:
            The retrieved integer, or None if the key doesn't exist.
        """
        return self.get(key, fn=int)

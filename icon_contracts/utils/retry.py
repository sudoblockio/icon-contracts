from functools import wraps
from time import sleep
from typing import Union, Type

from balanced_backend.log import logger


def retry(
        exception_to_check: Union[Type[Exception], tuple[Exception]],
        tries: int = 10,
        delay: int = 1,
        back_off: int = 2,
):
    """
    Retry calling the decorated function using an exponential backoff.
    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry
    :param exception_to_check: The exception to check. May be a tuple of exceptions to check
    :param tries: Number of times to try (not retry) before giving up
    :param delay: Initial delay between retries in seconds
    :param back_off: Back_off multiplier e.g. Value of 2 will double the delay each retry
    :param logger: Logger to use. If None, print
    """

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exception_to_check as e:
                    msg = "Retrying in %d seconds..." % mdelay
                    logger.warning(msg)
                    sleep(mdelay)
                    mtries -= 1
                    mdelay *= back_off
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry

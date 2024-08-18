"""
https://github.com/python/cpython/issues/66587
https://github.com/python/cpython/issues/53451
"""

import concurrent.futures as futures
import multiprocessing
import logging
import sys

logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.DEBUG)


def test(value):
    if value:
        sys.exit(123)


if __name__ == '__main__':

    # with multiprocessing.Pool(1) as pool:
    #     cases = [0, 1, 0]
    #     pool.map(test, cases)

    with futures.ProcessPoolExecutor(1) as executor:
        cases = [0, 1, 0]
        executor.map(test, cases)

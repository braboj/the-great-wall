"""
https://github.com/python/cpython/issues/66587
https://github.com/python/cpython/issues/53451
"""

import multiprocessing, logging
logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.DEBUG)

import sys

def test(value):
    if value:
        sys.exit(123)


if __name__ == '__main__':
    pool = multiprocessing.Pool(1)
    cases = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    pool.map(test, cases)

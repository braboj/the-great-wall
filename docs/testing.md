# Testing


## Instructions

Use [GitHub Actions] to run tests on each pull request. You can run these 
tests yourself as well. To do this, first install the test dependencies, if 
any, for the project:

[GitHub Actions]: https://github.com/braboj/the-great-wall/actions

```bash
pip install -r ./builder/tests/requirements.txt
pip install -r ./profiles/tests/requirements.txt

... install other requirements ...

```

And then run the tests:

```bash
python manage.py test
```

## Unit Tests

Unit tests are used to test individual components of the system in isolation.
These tests are written using the `unittest` module in Python and are located
in the `tests` directory of each app or component.

Some examples of unit tests in the project are:

* [test_manager.py](../builder/tests/test_manager.py)
* [test_configurator.py](../builder/tests/test_configurator.py)
* [tests.py](../profiles/tests/tests.py)
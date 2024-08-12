# How to contribute

We'd love to accept your patches and contributions to this project. There are
just a few small guidelines you need to follow.

1. First, read these guidelines. Before you begin making changes, state your 
intent to do so in an Issue. 
2. Then, fork the project. Make changes in your copy of the repository. Then open a pull request 
   once your changes are ready.
3. A discussion about your change will follow, and if accepted, your contribution
will be incorporated into the project codebase.

## Code reviews

All submissions, including submissions by project members, require review.
Consult [GitHub Help] for more information on using pull requests.

[GitHub Help]: https://help.github.com/articles/about-pull-requests/

## Code style

In general, the project follows the guidelines in the
[Google Python Style Guide].

In addition, the project follows a convention of:
- Maximum line length: 100 characters
- Indentation: 4 spaces
- PascalCase for function and method names.
- No type hints, as described in [PEP 484], to maintain compatibility with
Python versions < 3.5.
- Single quotes around strings, three double quotes around docstrings.

[Google Python Style Guide]: http://google.github.io/styleguide/pyguide.html
[PEP 484]: https://www.python.org/dev/peps/pep-0484

## Testing

Use [GitHub Actions] to run tests on each pull request. You can run these 
tests yourself as well. To do this, first install the test dependencies, if 
any, for the project:

[GitHub Actions]: https://github.com/braboj/randomgen/actions

```bash
pip install -r ./builder/tests/requirements.txt
pip install -r ./profiles/tests/requirements.txt
```

And then run the tests:

```bash
python manage.py test
```

## Linting

Please run lint on your pull requests to make accepting the requests easier.
To do this, run `pylint` or a similar tool in the root directory of the 
repository. Note that even if lint is passed, additional style changes 
to your submission may be made during merging.
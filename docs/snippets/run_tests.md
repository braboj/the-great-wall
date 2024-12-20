```yaml
# This workflow will install Python dependencies, run tests and lint
# with a single version of Python For more information see:
# https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python

name: Run Tests

# Controls when the action will run.
on:

  # Manual trigger
  workflow_dispatch:

  # Push event to the main branch
  push:
    branches: [ "main" ]

  # Pull request to the main branch
  pull_request:
    branches: [ "main" ]

# Set permissions for the workflow
permissions:
  contents: read

# Define the job that will run the tests
jobs:

  # Build job
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python 3.12.2
      uses: actions/setup-python@v3
      with:
        python-version: "3.12.2"
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        if [ -f ./builder/tests/requirements.txt ]; then pip install -r ./builder/tests/requirements.txt; fi
        if [ -f ./profiles/tests/requirements.txt ]; then pip install -r ./profiles/tests/requirements.txt; fi
    - name: Lint with flake8
      run: |
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    - name: Test with Django (unittest)
      run: |
        python manage.py test
```
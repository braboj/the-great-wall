## Solution Journal

### 1. Development Environment

| Category             | Details                   |
|----------------------|---------------------------|
| Programming Language | Python 3.12+              |
| Python IDE           | PyCharm Community Edition |
| Code style           | PEP-8, Google Doc Strings |
| Linting              | PyCharm built-in linter   |
| Testing              | Unittest                  |
| Version Control      | Git                       |
| Git Hosting          | GitHub                    |
| CI/CD                | GitHub Actions            |
| Documentation        | GitHub Pages, MkDocs      |


### 2. Project Requirements

### 2.1. Input

- The solution MUST provide a configuration file containing wall profiles. 
- The configuration file MUST contain one or more lines, each representing a 
  wall profile.
- Each profile MUST have one or more of sections with initial heights in feet
- Each section MUST have an initial height between 0 and 30 feet.
- Each section MUST be separated by a space
- The maximum allowed amount of sections is 2000
- The user MAY change the wall profiles at any time using the REST API 
  (add, update, delete)
- The user MAY switch between the multi-threaded and single-threaded 
  construction mode using the REST API

Example (config.ini): The following configuration file contains three wall
profiles with two sections each.

```ini
10 20
10 5
20 25
```

### 2.2. Output

- The app MUST provide an endpoint to get the daily status of the wall.
- The app MUST provide an endpoint to get an overview of the final cost of the 
  wall
- The app MUST provide an endpoint to get an overview of the final cost per 
  profile
- The app MUST store a log file that shows which thread is working on which 
  section
- The user may access the log files using the REST API


### 4. Proof of concept

In this step we will create a prototype of the solution to check our 
understanding of the problem. The prototype will be just a simple Python 
script that takes the configuration as a python list and prints the daily
status of the wall.

```python
def main():
    wall_profiles = [
        [10, 20],
        [10, 5],
        [20, 25]
    ]

    for day in range(1, 31):
        print(f"Day {day}")
        for profile in wall_profiles:
            for section in profile:
                print(f"Section: {section} Height: {section + day}")
        print()
```


### 5. Brainstorm the system design

### 7. Implement the REST API with Django

### 10. Implement unit tests for the backend

**Functional tests**

We will implement unit tests for the Backend using Pytest. We will cover each class
and method with unit tests to guarantee that the solution is working as expected. 

The testing discovered some bugs in the implementation that are related to the validation of the 
input parameters. 

**Performance tests**

We will implement performance tests to check the performance of the solution. We will use the
maximum number of random numbers to check the performance of the solution. Manual testing showed
that RandomGenV2 is around 3 times slower than RandomGenV1.

The task definition doesn't mention any performance requirements. We will assume that the solution
should be fast enough to generate random numbers in a reasonable time. A reasonable time for the 
backend is around 50 msec, bearing in mind that the REST API is going to stack on it and add
some latency.


### 13. Feedback from a beta tester

### 15. Docstrings

Now it is time to add docstrings to the classes and methods. We will use the
**_Google Docstring_** format. The docstrings will be used to generate the API 
manual.

### 16. Containerize the solution

### 17. Code review

### 18. Documentation

We will use MkDocs to build the documentation. The documentation will be
deployed to GitHub Pages. The documentation will contain at least the following
sections:

1. Problem
2. Solution
3. Installation
4. Rest API
5. CONTRIBUTING.md
6. README.md

### 19. Create the CI/CD pipeline

We will create a GitHub Actions workflow to run the tests on every push to the
main branch. We will also create a GitHub Actions workflow to build and push the
Docker image to Docker Hub on every release.

What we want:

1. Run the tests on every push to the main branch.
3. Build and push the Docker image to Docker Hub on each push.
4. Build the documentation and deploy it to GitHub Pages on every release.

### 20. Tag the first increment

Till now, we were in the pre-development phase. After the tag, changes will be
tracked using concrete issues in the commit messages.
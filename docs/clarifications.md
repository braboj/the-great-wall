# Clarification List

_This section is only for demonstrating the questions that arise during the
development. Typically, these questions are discussed with the client or the
team members in regular team meetings._ 

---
Q: The version of Python is not specified. Shall we write the solution to be
compatible with a version lower than 3.6 (annotations)?

A: We will provide compatibility with Python 3.6 and lower, meaning we will
not use annotations but provide type hints in the docstrings.

---
Q: The task has not specified whether to store the data in a database.
Shall we assume to solve the task without using a database and models?

A: We will design and implement the models, but they will not be connected to
the database as part of the MVP.

---
Q: Should we use the library `unittest` as a standard library for testing?

A: Yes, we will use the `unittest` library for testing, as it is a standard
library and is widely used in the Python community (including Django).

---
Q: How should we handle the errors in the REST API? Shall we use the Django
error handling mechanism or create a custom error handling mechanism?

A: We will use the Django error handling mechanism to handle the errors in the
REST API. The standard error will be 500 (Internal Server Error) for 
unexpected errors

---
Q: How is the user to interact with the solution configuration? Shall we use
a configuration file, command-line arguments or the REST API?

A: We will use a configuration file to store the wall profiles and the number
of teams available. The backend will read the configuration file and start the 
construction process. The results will be written to a log file. Both the 
configuration and log file will also be available through the REST API.

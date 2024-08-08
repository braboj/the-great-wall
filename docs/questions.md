# Clarification Questions

> This section is only for demonstrating the questions that arise during the
> development. Typically, these questions are discussed with the client or the
> team members in regular team meetings. 

1. The length of the wall is 300 miles, but it seems the length is not relevant
to the problem.
2. Are we obliged to use a database to store the wall profiles and sections?
3. Should we use the library `unittest` as a standard library for testing?
4. How is the user  to set the configuration file and the
log file? 
5. Can we ssume that the solution will not be assessed based on some 
   performance, e.g. response time?
6. Should we extend the `multiprocessing.get_logger()` to log tap the messages
from the library or focus on our custom logger?
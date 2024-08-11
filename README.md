# Overview

The project is a REST API to simulate and track the construction of a fictional 
defensive wall using `Django` and `multiprocessing`. This wall consists of
multiple sections, and the system should accurately track the progress, 
material usage, and costs associated with the construction.

# Installation

To get started, you need to install Docker. You can find the installation
instructions [here](https://docs.docker.com/engine/install/). After that, 
you can run the following command to get the project image:

```bash
docker pull braboj/wall_project:latest
```

And finally, you can run the following command to start the project:

```bash
docker run -p 8000:8000 braboj/wall_project:latest
```

To access the project, open your browser and go to

- [http://localhost:8080](http://localhost:8080). 

A simple page will be displayed with the endpoints available. As a quick 
example, use the following link to get the daily status of the wall:

```text
http://localhost:8080/profiles/1/days/1
```

# Next Steps
 - Check the [Wall Project Pages](https://braboj.github.io/wall_project/).
 - To contribute, please visit [Contributing](CONTRIBUTING.md)
 - To leave feedback, please visit [Discussions](https://github.com/braboj/the-great-wall/discussions)
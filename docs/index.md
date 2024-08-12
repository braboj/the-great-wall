# Introduction

This project is a REST API to simulate and track the construction of a fictional 
defensive wall using `Django` and `multiprocessing`. This wall consists of
multiple sections, and the system should accurately track the progress, 
material usage, and costs associated with the construction.

## Installation

To get started, you will need to install Docker. You can find the installation
instructions on this page:

- [Install Docker Engine](https://docs.docker.com/engine/install/). 

After that, you can run the following command to get the project image:

```bash
docker pull braboj/wall_project:latest
```

And finally, you can run the following command to start the project:

```bash
docker run -p 8080:8080 braboj/wall_project:latest
```

To access the project, open your browser and navigate to:

- [http://localhost:8080](http://localhost:8080)

A simple page will be displayed with the endpoints available. For more
information on the REST API, please visit:

- [REST API Reference](https://braboj.github.io/the-great-wall/rest_api/)

## Usage

Use the following links to check the solution with the examples from the 
prolem statement:

- [http://localhost:8080/profiles/overview](http://localhost:8080/profiles/overview)
- [http://localhost:8080/profiles/overview/1](http://localhost:8080/profiles/overview/1)
- [http://localhost:8080/profiles/1/overview/1)](http://localhost:8080/profiles/1/overview/1)
- [http://localhost:8080/profiles/1/days/1](http://localhost:8080/profiles/1/days/1)

Additionally, you can use the following links to check the logs and the 
configuration:

- [http://localhost:8080/profiles/logs](http://localhost:8080/profiles/logs)
- [http://localhost:8080/profiles/config](http://localhost:8080/profiles/config)


## Next Steps
 - Read the [Wall Project Pages](https://braboj.github.io/the-great-wall/)
 - Visit the [Wall Project Repository](https://github.com/braboj/the-great-wall)
 - To leave feedback, please visit [Discussions](https://github.com/braboj/the-great-wall/discussions)
 - To contribute, please visit [Contributing](https://github.com/braboj/the-great-wall/blob/main/CONTRIBUTING.md)
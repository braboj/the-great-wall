# Wall Project

To get started, you need to install Docker. You can find the installation
instructions [here](https://docs.docker.com/engine/install/). After that, you can run the following command to 
get the project image:

```bash
docker pull braboj/wall_project:latest
```

Then you can run the following command to start the project:

```bash
docker run -p 8000:8000 braboj/wall_project:latest
```

To use the solution, open your browser and go to

- [http://localhost:8080](http://localhost:8080). 

A simple page will be displayed with the endpoints available. As a quick 
example, use the following link to get the daily status of the wall:

```text
http://localhost:8080/profiles/1/days/1
```

Enjoy!
# User Manual


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

Open the browser and navigate to:

- [http://localhost:8080](http://localhost:8080)

A simple page will be displayed with the endpoints available. As a quick
example, use the following link to get the daily status of the wall:

- [http://localhost:8080/profiles/1/days/1](http://localhost:8080/profiles/1/days/1)

A simple page will be displayed with the endpoints available. For more
information on the REST API, please visit:

- [REST API Reference](https://braboj.github.io/the-great-wall/rest_api/)

## Web Interface

The project offers a REST API to interact with the simulation. The API is
documented in the [REST API Reference](https://braboj.github.io/the-great-wall/rest_api/).
It allows the user to track the construction process, to get the log entries
from the log file and to change the configuration of the simulation dymamically,
without the need to restart the simulation.

## Configuration File

Another option to change the parameters of the simulation without the need to 
change the source code. This is done by using a configuration file read at the 
start of the simulation.

The file is located in the `data` directory and is named `wall.ini`. After
a change of the configuration file, the simulation must be restarted to apply
the new parameters.

```ini
# ./data/wall.ini
[Construction]
volume_ice_per_foot = 195
cost_per_volume = 1900
target_height = 30
max_section_count = 2000

[Task]
num_workers = 20
cpu_worktime = 0.01

[Profiles]
21 25 28
17
17 22 17 19 17
```

## Logging

The project uses the Python `logging` module to log messages. The log entries
are stored in a file named `wall.log` in the `data` directory.
The user can access the log file through the REST API or by reading the file
directly.

```log
2024-08-12 21:41:29,246 INFO     Worker-66       - Added 1 foot to section 0 to reach 22 feet on day 1
2024-08-12 21:41:29,246 INFO     Worker-71       - Added 1 foot to section 1 to reach 26 feet on day 1
2024-08-12 21:41:29,247 INFO     Worker-67       - Added 1 foot to section 2 to reach 29 feet on day 1
2024-08-12 21:41:29,248 INFO     Worker-68       - Added 1 foot to section 3 to reach 18 feet on day 1
2024-08-12 21:41:29,249 INFO     Worker-65       - Added 1 foot to section 4 to reach 18 feet on day 1
2024-08-12 21:41:29,258 INFO     Worker-72       - Added 1 foot to section 5 to reach 23 feet on day 1
2024-08-12 21:41:29,307 INFO     Worker-67       - Added 1 foot to section 6 to reach 18 feet on day 1
2024-08-12 21:41:29,307 INFO     Worker-71       - Added 1 foot to section 7 to reach 20 feet on day 1
2024-08-12 21:41:29,308 INFO     Worker-66       - Added 1 foot to section 8 to reach 18 feet on day 1
```

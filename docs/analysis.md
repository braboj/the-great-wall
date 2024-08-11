# Problem Analysis


## 1. Scope

The goal is to develop a REST API to simulate and track the construction of 
a fictional defensive wall using the Django framework, Django Rest Framework 
(DRF) and the multiprocessing library. This wall consists of multiple sections, 
and the system should accurately track the progress, material usage, and costs 
associated with the construction.

## 2. Features

- REST API to track the construction of the wall
- Multiprocessing to simulate the construction of the wall
- Logging to track the progress of the construction
- Configurable wall profiles and work crews

## 3. Requirements

The requirements are divided into three categories based on RFC 2119:

- `MUST`   - Task that is critical to the solution
- `SHOULD` - Task that is important but not critical to the solution
- `MAY`  - Task that is optional

### 3.1. Construction Algorithm

- Each foot added to a section uses 195 cubic yards of ice.
- Processing one cubic yard of ice costs 1900 Gold Dragon coins.
- Construction crews work simultaneously on all sections that are below 30 
  feet in height. Once a section reaches 30 feet, its crew is relieved.
- After the crew is relieved, it can be reallocated to another section of 
  the wall (relocate mode)

### 3.2. Technology Stack

- `MUST` - Use **Django and Django Rest Framework**
- `MUST` - Use **Docker** to containerize the solution
- `MUST` - Use **unittest** to test the solution
- `SHOULD` - Use Python 3.12+
- `MAY` - Use SQLite as the database for persistence

### 3.3. Input

- `MUST` - Provide a file containing wall profiles. 
- `MUST` - The file contains one or lines for each wall profile
- `MUST` - Each profile has one or more of sections with initial heights
- `MUST` - Each section has an initial height between 0 and 30 feet.
- `MUST` - Each section is separated by a space
- `MUST` - The maximum allowed number of sections is 2000
- `MAY` - The user MAY change the wall profiles using the REST API
- `MAY` - The user MAY adjust the number of crews using the REST API
 
### 3.4. Output

- `MUST` - Return JSON response for all API endpoints
- `MUST` - Provide an endpoint to get the daily status of the wall
- `MUST` - Provide an endpoint to get the total cost of the wall
- `MUST` - Provide an endpoint to get the cost of a specific profile
- `MUST` - Store a log file showing the work done by the teams
- `MAY` - User may access the log files using the REST API

### 3.5. Examples

#### Input

```
21 25 28
17
17 22 17 19 17
```

On the first day, all crews work simultaneously, each adding 1 foot to their 
section:

- First profile: 3 crews x 195 = 585 cubic yards
- Second profile: 1 crew x 195 = 195 cubic yards
- Third profile: 5 crews x 195 = 975 cubic yards
- In total: 1 755 cubic yards

On the second day, it’s the same. However, the last section of the first 
wall profile reaches 30 feet and its crew is being relieved. 

- First profile: 3 crews x 195 = 390 cubic yards
- Second profile: 1 crew x 195 = 195 cubic yards
- Third profile: 5 crews x 195 = 975 cubic yards


On the third day, only two crews work from the first wall profile:

- First profile: 2 crews x 195 = 390 cubic yards
- Second profile: 1 crew x 195 = 195 cubic yards
- Third profile: 5 crews x 195 = 975 cubic yards

And so on until all sections reach 30 feet...

#### Output

```text
# ----------------------------------------------------------
# Get the ice amount used on a given day for a given profile
# ----------------------------------------------------------

GET /profiles/1/days/1/
RETURNS: {
day: ”1”;
ice_amount: “585”
}

# ----------------------------------------------------------
# Get the total cost used on a given day for a given profile
# ----------------------------------------------------------

GET /profiles/1/overview/1/
RETURNS: {
day: ”1”;
cost: “1,111,500”
}

# ----------------------------------------------------------
# Get the total cost used on a given day for all profiles
# ----------------------------------------------------------

GET /profiles/overview/1/
RETURNS: {
day: ”1”;
cost: “3,334,500”
}

# ----------------------------------------------------------
# Get the total cost used on all days for all profiles
# ----------------------------------------------------------

GET /profiles/overview/
RETURNS: {
day: None;
cost: “32,233,500”
}
```

### 4. Minimum Viable Product (MVP)

The MVP should include the following features:

- Builder and configuration components
- Models will be provided but not used (use only in-memory storage)
- Routing and views for the API
- Dockerfile to build the image
- Unit tests for the API
- Documentation for the solution

Excluded are the following features:
- Database persistence for the wall profiles
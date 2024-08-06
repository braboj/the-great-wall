## Problem Statement


### Background

The Wall is a colossal fortification intended to defend a realm from 
external threats. It stretches for 300 miles along the northern border and 
is built using solid ice. Each section of the Wall has a dedicated 
construction crew tasked with increasing the section's height by 1 foot 
each day until it reaches a total height of 30 feet.


### Objectives

The goal is to develop a REST API to simulate and track the construction of 
a fictional defensive wall using the Django framework and Django Rest 
Framework (DRF). This wall consists of multiple sections, and the system 
should accurately track the progress, material usage, and costs associated 
with the construction.

### Construction Process

- Each foot added to a section uses 195 cubic yards of ice.
- Processing one cubic yard of ice costs 1900 Gold Dragon coins.
- Construction crews work simultaneously on all sections that are below 30 
  feet in height. Once a section reaches 30 feet, its crew is relieved.


### Construction Mode

1. **Single-threaded**: Unlimited number of construction crews, just calculate
the cost and the daily progress of the wall.
2. **Multi-threaded**: Limited number of construction crews that can be 
reallocated to different sections of the wall. 

### Questions

- The length of the wall is 300 miles, but it seems the length is not relevant
to the problem.
- It is not clear how to allow the user to switch between the
multithreaded and single-threaded construction mode. Shall it be done using
the REST API?
# Level 1 
In this first level, we will implement a geographic search engine. 

We have a list of campers. Each camper has a location
 (`latitude` and `longitude`).
We also have a list of searches. Each search also have a location
 (`latitude`and `longitude`). 
To filter the campers, we must use a bounding box that is
 2 degrees square in total (ie, +/-0.1 from each coordinate). 

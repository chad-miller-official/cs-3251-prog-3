# CS 3251 Programming Assignment 3
Christopher Deese - cdeese27@gatech.edu - Section A
Chad Miller - cmiller86@gatech.edu - Section B
4/21/2017 - Programming Assignment 3 - Distance vector routing
# Files
./sample.txt - sample output of the program
./src - all source code
...event.py - holds a queue of all events from the given events file, and contains methods to get events from the queue as needed
...graph.py - represents the graph of the current network, provides methods to retrieve edges and vertices and their neighbors
...router.py - holds the routing table, least cost pointers, hop numbers, and next hops for all paths, plus getters/setters
...simulator.py - executable for the program, which parses input files and runs the simulation for the three algorithms
./test - this folder contains 3 sets of topography and events text files we used for testing
# Compiling and Running
No need to compile - it's all in python.
To run, correct usage is
    `python3 ./simulator.py <topology file> <event file> <verbose value>`
Where verbose is a binary flag, 0 for non-verbose output, 1 for verbose output.
# Limitations and Bugs

# CS 3251 - Distance Vector Routing 04/21/2017

## Project Group

Christopher Deese - cdeese27@gatech.edu - Section A
Chad Miller - cmiller86@gatech.edu - Section B

## Files

### sample.txt

Sample output of the program. From top-to-bottom, lists the command that was run, the
contents of the input files supplied for the program, and the contents of the three files
that were output by the program.

### src/event.py

Defines a class that implements a queue for all events specified in the given network
events file. Contains methods to get events from the queue as needed.

### src/graph.py

Defines a class that represents an undirected graph of the network specified in the
topology file. Provides methods to retrieve edges and vertices and their neighbors.

### src/router.py

Defines a class that represents a routing table on steroids, which contains
least-cost pointers, hop counts, the immediate next hops for all paths, getters
and setters, and the routing table itself as a 2D array.

### src/simulator.py

The program main's executable, which parses input files and runs a simulation of
the following three variants of the distance-vector algorithm:

* Basic routing
* Split-horizon routing
* Split-horizon routing with poison reverse

The output for each algorithm is output to its own file, which is created in the
directory from which the program was run.

# Compiling and Running

No need to compile - it's all in Python.

To run from the root directory, the correct usage is:

`python3 src/simulator.py <topology file> <event file> <verbose value>`

Where verbose is a binary flag, 0 for non-verbose output, 1 for verbose output.

If the verbose flag is 0, the following three files are output, which correspond
to their namesake algorithm variants:

* output-basic.txt
* output-split-horizon.txt
* output-split-horizon-with-poison-reverse.txt

If the verbose flag is 1, the following three files are output instead:

* output-basic-detailed.txt
* output-split-horizon-detailed.txt
* output-split-horizon-with-poison-reverse.txt

# Limitations and Bugs

No limitations or bugs are known. However, if any are found, please notify
either Chris or Chad.

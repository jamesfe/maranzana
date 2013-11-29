Maranzana Heuristic
==================

For Finding Centers in Weighted Network Graphs
----------------------------------------------

This script reads a text file describing distances between nodes; it acquires weights for each node, and utilizes Maranzana's heuristic to identify a set of centers that have the shortest distance, weighted by the forementioned weights, to each other node.  Default is 2 nodes. 

Synopsis of the algorithm:
--------------------------

- 1. Load distance tables, weight tables, etc.
- 2. Begin permutations: 
- 2a. Seed Facilities (array)
- 2b. Assign nodes to seeds
- 2c. Calculate new facilties to replace seeds
- 3. Repeat 2 until nothing changes

Task List:
----------

- [ ] Move weights to input textfile and out of script
- [ ] Better code commenting
- [ ] Output in D3.js-compatible JSON file

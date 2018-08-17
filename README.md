# traj-graph-align

This python package is meant to be expanded to produce local alignments of single cell trajectory graphs. 

This package has three sub modules concerned with trajectory alignment: 1.) milestone similarity 2.) local graph alignment 3.) read and write functions for the inputs and output of 1 and 2.

A major draw back of this technique is the necesity to extract a reliable graph representation from the output of trajectory inference algorithms. Also, developing a sufficiently accurate measure for node to node similarities on different datasets is both integral and challenging.

The alternative method of segmenting trajectories in to branches and using a combination of marker genes, pseudotime assignment, and dynamic time warping is being developed [here](https://github.com/Stuartlab-UCSC/traj-branch-align). 



#!/usr/bin/env bash


QF=$1
RF=$2
# Query graph in weighted edgelist format
Q=$3
# Reference graph in weighted edgelist format
R=$4
# All nodes and their xy coods, tab delim
X=$5
# OUtput.js file
O=$6
node_sim-calc.py -X $QF -Y $RF -o sim.out

align_mcl.py -q $Q -r $R -s sim.out -o align.out

alignmentFilesToJSExport.py -q $Q -r $R -x $X -s sim.out -a align.out -o $O

 #../simtojs.sh ../../data/graphs/wel/t-q.wel  ../../data/graphs/wel/mock-ref.wel ../../data/layouts/xys/ref.xys.tab trash.js

#ubt-q.wel
#
# linear 6, similarities are way off
# simtojs.sh ../data/features/q-l6.f50.tab ../data/features/50_rand_features-ref_graph.tab ../data/graphs/wel/l6-q.wel  ../data/graphs/wel/mock-ref.wel ../data/layouts/xys/all.mock.xys.tab /home/duncan/trajectory/react-svg-graph/src/data/trash.js

# ubt
# simtojs.sh ../data/features/q-ubt.f50.tab ../data/features/50_rand_features-ref_graph.tab ../data/graphs/wel/ubt-q.wel  ../data/graphs/wel/mock-ref.wel ../data/layouts/xys/all.mock.xys.tab /home/duncan/trajectory/react-svg-graph/src/data/ubt.js

# simtojs.sh ../data/features/q-l6.f50.tab ../data/features/50_rand_features-ref_graph.tab ../data/graphs/wel/l6-q.wel  ../data/graphs/wel/mock-ref.wel ../data/layouts/xys/all.mock.xys.tab /home/duncan/trajectory/react-svg-graph/src/data/l-true-cheat.js
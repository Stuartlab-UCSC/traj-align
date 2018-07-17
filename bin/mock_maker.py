"""
 script that makes a "reference" graph that simply takes a bunch of
 smaller graphs, makes layouts for them and then makes a larger "reference"
 layout by putting each of the graphs onto a grid. Here, its hard coded
 that its a 3x3 grid, with 8 of the sections filled out.

 Anyway if you have to make another random layout this might be a good
 start.
"""
import networkx as nx
import pandas as pd

path="/home/duncan/trajectory/traj-restapi/data/toy-graphs/"
filenames = [
    "cycle-12.ef",  "cycle-6.ef", "linear-4.ef", "tree-depth3.ef",
    "unbalanced-tree-depth3.ef", "cycle-4.ef", "linear-12.ef", "linear-6.ef"
]
G  = nx.Graph()
graphs=[]
for filename in filenames:
    print filename
    graphs.append(read_type(path+filename, type="edgelist"))
    G = nx.union(G, read_type(path+filename, type="edgelist"))

increment = 3
graph_pos=[]
XYS=pd.DataFrame()
col=0
for square, G in enumerate(graphs):
    row = square / 3 # Rounds down to nearest whole number.
    col+=1
    if col==3:
        col=0
    xoffset = row * increment
    yoffset = col * increment
    layout = nx.spring_layout(G)
    nx.draw_spring(G)
    print(filenames[square])
    plt.savefig("./data/" + filenames[square] +".jpg")
    plt.gcf().clear()
    xys = pd.DataFrame(map(lambda x: layout[x], layout), index=layout.keys())
    xys[0] = xys[0] + xoffset
    xys[1] = xys[1] + yoffset
    XYS=XYS.append(xys)

import spatial # This is a tumor map module can be found here: https://github.com/ucscHexmap/compute/tree/master/calc
dist = pd.DataFrame(spatial.inverseEucDistance(XYS),index=XYS.index, columns=XYS.index)
dist.to_csv("./fref-self_dist-springlayout.tab", sep="\t")
XYS.to_csv("./fref-springlayout_with_offset.xys.tab", sep="\t")
dist.iloc[40].sort_values()

import argparse
import random
from collections import namedtuple
from typing import List

import networkx as nx
import matplotlib.pyplot as plt

Message = namedtuple('Message', ())
Measure = namedtuple('Measure', ('step', 'count'))

parser = argparse.ArgumentParser(description='Simulates "broadcast storm" and shows growth plot of messages in it.\n'
                                             'Be careful with arguments, messages grow really fast.')
parser.add_argument('-n', '--vertices', type=int, nargs='?', default=3,
                    help='amount of vertices in network of complete graph')
parser.add_argument('-s', '--steps', type=int, nargs='?', default=6,
                    help='amount of steps in a simulation')

args = parser.parse_args()

steps = args.steps
n = args.vertices
initiator = random.randrange(n)

Net = nx.complete_graph(n)
for node, attributes in Net.nodes.items():
    attributes['messages'] = [] if node != initiator else [Message()]

message_count = 1
results: List[Measure] = [Measure(step=0, count=1)]
for i in range(1, steps):
    for node, p_attrs in Net.nodes(data=True):
        for neighbour in Net[node]:
            c_attrs = Net.node[neighbour]
            c_attrs['messages'].extend(p_attrs['messages'])
            message_count += len(p_attrs['messages'])
        p_attrs['messages'] = []
    results.append(Measure(step=i, count=message_count))

plt.plot(*zip(*results))
plt.show()

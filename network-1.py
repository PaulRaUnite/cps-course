import argparse
import random
from typing import List

import matplotlib.pyplot as plt
import networkx as nx

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
    attributes['messages'] = int(node == initiator)

message_count = 1
results: List[int] = [1]
for i in range(1, steps):
    for node, p_attrs in Net.nodes(data=True):
        for neighbour in Net[node]:
            c_attrs = Net.node[neighbour]
            c_attrs['messages'] += p_attrs['messages']
            message_count += p_attrs['messages']
        p_attrs['messages'] = 0
    results.append(message_count)

print(results)
plt.plot(list(range(steps)), results)
plt.show()

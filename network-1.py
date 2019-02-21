import argparse
import random
from typing import List

import matplotlib.pyplot as plt
import networkx as nx

parser = argparse.ArgumentParser(description='Simulates "broadcast storm" and shows growth plot of messages in it.\n'
                                             'Be careful with arguments, messages grow really fast.')
parser.add_argument('-n', '--vertices', type=int, nargs='?', default=5,
                    help='amount of vertices in network of complete graph')
parser.add_argument('-s', '--steps', type=int, nargs='?', default=10,
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
    for node, parent_attrs in Net.nodes(data=True):
        parent_messages = parent_attrs['messages']
        parent_attrs['messages'] = 0
        message_count -= parent_messages
        for neighbour in Net[node]:
            c_attrs = Net.node[neighbour]
            c_attrs['messages'] += parent_messages
            message_count += parent_messages
    results.append(message_count)

print('Step message counts: ', ', '.join(map(str, results)))
plt.plot(list(range(steps)), results)
plt.show()

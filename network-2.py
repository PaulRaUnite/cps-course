import argparse
import random
from collections import namedtuple
from itertools import count

import matplotlib.pyplot as plt
import networkx as nx

Message = namedtuple('Message', ())

parser = argparse.ArgumentParser(description='Simulates "broadcast storm" but nodes do not repeat the message again.')
parser.add_argument('-n', '--vertices', type=int, nargs='?', default=5,
                    help='amount of vertices in network of complete graph')
parser.add_argument('-p', '--probability', type=float, nargs='?', default=0.4,
                    help='probability of edge generation')

args = parser.parse_args()

prob = args.probability
n = args.vertices
initiator = random.randrange(n)

Net: nx.DiGraph = nx.fast_gnp_random_graph(n, prob, directed=True)
for node, attrs in Net.nodes.items():
    attrs['sent'] = node == initiator

message_counter = 0
for (source, target), channel in Net.edges.items():
    if source == initiator:
        channel['messages'] = 1
        message_counter += 1
    else:
        channel['messages'] = 0
    channel['color'] = 'black'

results = []
for i in count():
    results.append(message_counter)
    if not message_counter:
        break
    for (source, repeater), downstream in Net.edges.items():
        messages = downstream['messages']
        message_counter -= messages
        if messages and not Net.nodes[repeater]['sent']:
            downstream['color'] = 'blue'
            for target, upstream in Net[repeater].items():
                upstream['messages'] += 1
            message_counter += len(Net[repeater])
            Net.nodes[repeater]['sent'] = True
        downstream['messages'] = 0

plt.show()

plt.subplot(1, 2, 1)
pos = nx.circular_layout(Net)
nx.draw(Net, pos, node_color=['blue' if node == initiator else 'magenta' for node in Net.nodes],
        edge_color=[attrs['color'] for _, attrs in Net.edges.items()])
plt.title('Net')

plt.subplot(1, 2, 2)
plt.plot(list(range(len(results))), results)
plt.xlabel('Steps')
plt.ylabel('Messages')

plt.show()

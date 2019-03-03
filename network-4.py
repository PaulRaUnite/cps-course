import argparse
import random
from collections import Counter
from itertools import count, chain
from typing import Dict, Mapping

import matplotlib.pyplot as plt
import networkx as nx

from utils import complement_edges

parser = argparse.ArgumentParser(description='Simulates "broadcast storm" but nodes do not repeat the message again.')
parser.add_argument('-v', '--vertices', type=int, nargs='?', default=5,
                    help='amount of vertices in network of complete graph, default is 5')
parser.add_argument('-p', '--probability', type=float, nargs='?', default=0.4,
                    help='probability of edge generation, default is 0.4')
parser.add_argument('-n', '--steps', type=int, nargs='?', default=100,
                    help='number of steps in simulation, default is 100')
parser.add_argument('-b', '--broadcast', type=float, nargs='?', default=0.2,
                    help='broadcast spawn probability, default is 0.2')
parser.add_argument('-s', '--seed', type=int, nargs='?', default=None,
                    help='seed of generation, use it if you want to reproduce some outcome, '
                         'other characteristics should be the same too')
parser.add_argument('-d', '--debug', type=bool, nargs='?', default=False,
                    help='print statistics')

message_type = count()

args = parser.parse_args()

prob = args.probability
v = args.vertices
seed = args.seed
steps = args.steps
broadcast_probability = args.broadcast
debug = args.debug

if not seed:
    seed = random.randrange(9999)
print("Seed: ", seed)
random.seed(seed)
initiator = random.randrange(v)

Net: nx.DiGraph = nx.fast_gnp_random_graph(v, prob, directed=True)
complement_edges(Net)
for node, attrs in Net.nodes.items():
    attrs['broadcast_table']: Dict[int, int] = {}

for _, channel in Net.edges.items():
    channel['sent'] = []
    channel['planned'] = []


def launch_broadcast_from(node):
    message = next(message_type)
    if debug:
        print("Initiator: ", node, ", message: ", message)
    for _, channel in Net[node].items():
        channel['sent'].append(message)
    Net.nodes[node]['broadcast_table'][message] = 2


def try_to_launch_new_broadcast():
    initiator = random.randrange(v * int(1 / broadcast_probability))
    if initiator < v:
        launch_broadcast_from(initiator)


def process_messages():
    for (source, repeater), downstream in Net.edges.items():
        for message in downstream['sent']:
            if message in Net.nodes[repeater]['broadcast_table']:
                continue
            for target, upstream in Net[repeater].items():
                if target == source:
                    continue
                upstream['planned'].append(message)
            Net.nodes[repeater]['broadcast_table'][message] = 2
    for node, attrs in Net.nodes.items():
        attrs['broadcast_table'] = {
            message: live_time - 1 for message, live_time in attrs['broadcast_table'].items() if live_time != 0
        }
    for _, channel in Net.edges.items():
        channel['sent'] = channel['planned']
        channel['planned'] = []


def collect_results() -> (Mapping[int, int], int):
    return Counter(chain.from_iterable(ch['sent'] for ch in Net.edges.values())), \
           sum(len(node_data['broadcast_table']) for node_data in Net.nodes.values())


launch_broadcast_from(initiator)
statistics = [collect_results()]
for _ in range(steps):
    try_to_launch_new_broadcast()
    process_messages()
    r = collect_results()
    if debug:
        print(r)
    statistics.append(r)

plt.subplot(1, 2, 1)
pos = nx.circular_layout(Net)
nx.draw(Net, pos, with_labels=True)
plt.title('Net')

x = list(range(steps + 1))
lines_data = {m: [] for m in range(next(message_type))}
for message_count, table_length in statistics:
    for message, count in lines_data.items():
        count.append(message_count.get(message, 0))

plt.subplot(1, 2, 2)
for message, count in lines_data.items():
    plt.plot(x, count, label="message {}".format(message))

plt.plot(x, [table_length for _, table_length in statistics], linestyle='-.', label="General length of message tables.")
plt.legend()
plt.xlabel('Steps')
plt.ylabel('Messages')

plt.show()

import networkx as nx


def complement_edges(graph: nx.DiGraph):
    new_edges = []
    for e in graph.edges:
        new_edges.append(e)
        new_edges.append(tuple(reversed(e)))
    graph.add_edges_from(new_edges)

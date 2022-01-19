from collections import defaultdict
from typing import Any
from typing import Dict, List
from enum import Enum
from typing import Optional

class EdgeType(Enum):
    directed = 1
    undirected = 2


class Vertex:
    data: Any
    index: int

    def __init__(self, data, index):
        self.data = data
        self.index = index


class Edge:
    source: Vertex
    destination: Vertex
    weight: Optional[float]

    def __init__(self, source1, destination1, weight1):
        self.source = source1
        self.destination = destination1
        self.weight = weight1

    def __repr__(self):
        return "{}: v{} w={}".format(self.destination.index, self.destination.data, self.weight)


class Graph:
    adjacencies: Dict[Vertex, List[Edge]]

    def __init__(self):
        self.adjacencies = dict()
        self.edges = defaultdict(list)
        self.distances = {}

    def create_vertex(self, data: Any):
        self.adjacencies[Vertex(data, len(self.adjacencies))] = list()
        self.x = [[0 for i in range(len(self.adjacencies))] for j in range(len(self.adjacencies))]

    def add_directed_edge(self, source: Vertex, destination: Vertex, weight: Optional[float] = None) -> None:
        if source not in self.adjacencies:
            self.adjacencies[Vertex(source.data, len(self.adjacencies))] = list()
        if destination not in self.adjacencies:
            self.adjacencies[Vertex(destination.data, len(self.adjacencies))] = list()
        self.adjacencies[source].append(Edge(source, destination, weight))
        self.edges[source.data].append(destination.data)
        self.distances[(source.data, destination.data)] = weight

    def add_undirected_edge(self, source: Vertex, destination: Vertex, weight: Optional[float] = None) -> None:
        if source not in self.adjacencies:
            self.adjacencies[Vertex(source.data, len(self.adjacencies))] = list()
        if destination not in self.adjacencies:
            self.adjacencies[Vertex(destination.data, len(self.adjacencies))] = list()
        self.adjacencies[source].append(Edge(source,destination,weight))
        self.adjacencies[destination].append(Edge(destination, source, weight))
        self.edges[source.data].append(destination.data)
        self.edges[destination.data].append(source.data)
        self.distances[(source.data, destination.data)] = weight
        self.distances[(destination.data, source.data)] = weight

    def add(self, edge: EdgeType, source: Vertex, destination: Vertex, weight: Optional[float]):
        if edge.name == 'directed':
            self.add_directed_edge(source, destination, weight)
        else:
            self.add_undirected_edge(source, destination, weight)

    def __repr__(self):
        temp = ""
        for x in self.adjacencies:
            temp = temp + "{}: v{} ----> {} \n".format(x.index, x.data, self.adjacencies[x])
        return temp

def all_weighted_shortest_paths(g: Graph, start: Any):
    poprzednik=[]
    for x in g.adjacencies:
        poprzednik.append(x.data)

    odwiedzane = [start]
    # print(poprzednik)
    poprzednik = {node: node for node in poprzednik}
    # print(poprzednik)
    weight = {node: float('+Inf') for node in poprzednik}
    weight[start] = 0

    while odwiedzane:
        u = odwiedzane.pop(0)

        for v in g.edges[u]:
            # print(v)
            # print(g.edges[u])
            # print(weight[u])
            weight2 = weight[u] + g.distances[(u, v)]
            # print(v)
            # print(u)
            # print(g.distances[(u,v)])
            if weight[v] == "Inf" or weight2 < weight[v]:
                weight[v] = weight2
                poprzednik[v] = u
                odwiedzane.append(v)

    def backtrace(node):
        path = []
        while poprzednik[node] != node:
            paths = []
            node1 = node
            node = poprzednik[node]
            paths.append(node)
            paths.append(node1)
            path.append(paths)
        return list(reversed(path))


    paths = {node: backtrace(node) for node in poprzednik}

    return paths


graph1 = Graph()
graph1.create_vertex(0)
graph1.create_vertex(1)
graph1.create_vertex(2)
graph1.create_vertex(3)
graph1.create_vertex(4)
graph1.create_vertex(5)

keys = [x for x in graph1.adjacencies.keys()]

graph1.add(EdgeType(2), keys[0], keys[1], weight=1)
graph1.add(EdgeType(2), keys[0], keys[5], weight=3)
graph1.add(EdgeType(2), keys[2], keys[1], weight=2)
graph1.add(EdgeType(2), keys[2], keys[3], weight=5)
graph1.add(EdgeType(2), keys[3], keys[4], weight=2)
graph1.add(EdgeType(2), keys[4], keys[1], weight=4)
graph1.add(EdgeType(2), keys[4], keys[5], weight=4)
graph1.add(EdgeType(2), keys[5], keys[2], weight=2)

print(all_weighted_shortest_paths(graph1,1))

graph2 = Graph()
graph2.create_vertex(0)
graph2.create_vertex(1)
# graph2.create_vertex(2)
graph2.create_vertex(3)
graph2.create_vertex(4)

keys2 = [x for x in graph2.adjacencies.keys()]

graph2.add(EdgeType(2), keys2[0], keys2[1], weight=1)   #0,1
graph2.add(EdgeType(2), keys2[3], keys2[0], weight=5)   #4,0
graph2.add(EdgeType(2), keys2[2], keys2[3], weight=2)   #3,4
graph2.add(EdgeType(2), keys2[3], keys2[1], weight=5)   #4,1

print(all_weighted_shortest_paths(graph2,3))

graph3 = Graph()
graph3.create_vertex(0)
graph3.create_vertex(1)
graph3.create_vertex(2)
graph3.create_vertex(3)
graph3.create_vertex(4)

keys3 = [x for x in graph3.adjacencies.keys()]

graph3.add(EdgeType(2), keys3[0], keys3[1], weight=1)
graph3.add(EdgeType(2), keys3[2], keys3[3], weight=5)
graph3.add(EdgeType(2), keys3[3], keys3[4], weight=2)
graph3.add(EdgeType(2), keys3[4], keys3[1], weight=4)
graph3.add(EdgeType(2), keys3[4], keys3[0], weight=1)

print(all_weighted_shortest_paths(graph3,0))

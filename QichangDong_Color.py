from collections import defaultdict
from typing import List, Tuple

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = {i: set() for i in range(self.V)}
        self.domains = {i: [] for i in range(self.V)}

    def add_edge(self, v, w):
        if w not in self.graph[v]:
            self.graph[v].add(w)
            self.graph[w].add(v)

    def set_domains(self, colors: int):
        for vertex in self.graph:
            self.domains[vertex] = list(range(1, colors + 1))

def ac3(graph):
    queue = [(x, y) for x in graph.graph for y in graph.graph[x]]
    while queue:
        x, y = queue.pop(0)
        if remove_inconsistent_values(graph, x, y):
            for neighbor in graph.graph[x]:
                if neighbor != y:
                    queue.append((neighbor, x))
    return True

def remove_inconsistent_values(graph, x, y) :
    removed = False
    for color in graph.domains[x]:
        if len(graph.domains[y]) == 1 and graph.domains[y][0] == color:
            graph.domains[x].remove(color)
            removed = True
            if len(graph.domains[x]) == 0:
                return False
    return removed

def lcv(graph, vertex):
    return sorted(graph.domains[vertex], key=lambda color: sum(1 for neighbor in graph.graph[vertex] if color in graph.domains[neighbor]))

def is_safe(graph, v, color, c):
    for neighbor in graph.graph[v]:
        if color[neighbor] == c:
            return False
    return True

def graph_coloring_util(graph, m, color, v):
    if v == graph.V:
        return True
    for c in lcv(graph, v):
        if is_safe(graph, v, color, c):
            color[v] = c
            if graph_coloring_util(graph, m, color, v + 1):
                return True
            color[v] = 0
    return False

def graph_coloring(graph, m):
    graph.set_domains(m)
    ac3(graph)
    color = [0] * graph.V
    if not graph_coloring_util(graph, m, color, 0):
        return None
    return color

def read_input(input_name):
    with open(input_name, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines if not line.startswith('#') and line.strip() != '']
    colors = int(lines[0].split('=')[1].strip())
    edges = [tuple(map(int, edge.split(','))) for edge in lines[1:]]

    return colors, edges

def read_file(input_file):
    graph = []
    with open(input_file, 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            elif line.lower().startswith('colors = '):
                color = int(line.split('=')[1].strip())
                color = set(range(1,color+1,1))
            else:
                x, y = line.strip().split(',')
                graph.append([int(x),int(y)])
    return color, graph

def test(result_dict,input_file):
    color, graph = read_file(input_file)
    for element in graph:
        if result_dict[element[0]] == result_dict[element[1]]:
            print("something is wrong")
    print("everything look good")

def main():
    try:
        input_name = "CSPinput1.txt"
        colors, edges = read_input(input_name)
        vertices = set()
        for edge in edges:
            vertices.add(edge[0])
            vertices.add(edge[1])
        graph = Graph(max(vertices)+1)
        for edge in edges:
            graph.add_edge(edge[0], edge[1])
        result = graph_coloring(graph, colors)
        result_dict = {}
        if result:
            for element in vertices:
                result_dict [element] = result[element]
        else:
            print("No solution exists.")
        test(result_dict,input_name)
        print(result_dict)
    except:
        print("No Solution found")

if __name__ == "__main__":
    main()

import heapq
import sys

class Graph:
    def __init__(self, file_path):
        self.adj_matrix = self.read_file(file_path)

    def read_file(self, file_path):
        with open(file_path) as f:
            lines = f.readlines()
            n = int(lines[0].strip())
            adj_matrix = [[int(x) for x in line.split()] for line in lines[1:]]
            return adj_matrix

    def get_vertex_num(self):
        return len(self.adj_matrix)

    def get_edge_weight(self, u, v):
        return self.adj_matrix[u][v]

    def get_neighbors(self, u):
        return [v for v in range(self.get_vertex_num()) if self.adj_matrix[u][v] > 0]

class MinHeap:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def branch_and_bound(graph):
    n = graph.get_vertex_num()
    unvisited = set(range(n))
    # Priority queue of (cost, (path, unvisited_set))
    queue = MinHeap()
    queue.put(([], unvisited), 0)
    # Initialize best path and its cost
    best_path = None
    best_cost = sys.maxsize
    while not queue.is_empty():
        # Get the lowest-cost path from the queue
        path, unvisited = queue.get()
        # Check if the path is complete
        if len(path) == n:
            # Calculate the cost of the path
            cost = sum(graph.get_edge_weight(path[i], path[i+1]) for i in range(n-1)) + graph.get_edge_weight(path[-1], path[0])
            # Update the best path if this one is better
            if cost < best_cost:
                best_path = path
                best_cost = cost
        else:
            # Add a new vertex to the path
            for v in unvisited:
                new_path = path + [v]
                new_unvisited = unvisited - {v}
                # Calculate a lower bound on the cost of the new path
                lb = sum(graph.get_edge_weight(new_path[i], new_path[i+1]) for i in range(len(new_path)-1))
                if lb < best_cost:
                    # Add the new path to the queue
                    queue.put((new_path, new_unvisited), lb)
    return best_path, best_cost

if __name__ == "__main__":
    file_path = "input.txt"
    graph = Graph(file_path)
    path, cost = branch_and_bound(graph)
    print("Найкращій шлях:", path)
    print("Вага:", cost)
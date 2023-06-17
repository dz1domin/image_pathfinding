import numpy as np
import heapq


def create_graph_from_image(image):
    rows, cols = image.shape[:2]
    graph = np.zeros((rows, cols), dtype=np.float32)

    for i in range(rows):
        for j in range(cols):
            if i > 0:
                graph[i, j] += abs(int(image[i, j]) - int(image[i - 1, j]))
            if i < rows - 1:
                graph[i, j] += abs(int(image[i, j]) - int(image[i + 1, j]))
            if j > 0:
                graph[i, j] += abs(int(image[i, j]) - int(image[i, j - 1]))
            if j < cols - 1:
                graph[i, j] += abs(int(image[i, j]) - int(image[i, j + 1]))

    return graph


def find_fastest_path(graph, start, end):
    rows, cols = graph.shape[:2]
    heap = [(0, start)]
    visited = set()
    prev = {}

    while heap:
        cost, node = heapq.heappop(heap)

        if node == end:
            break

        if node in visited:
            continue

        visited.add(node)

        row, col = node
        neighbors = []

        if row > 0:
            neighbors.append((row - 1, col))
        if row < rows - 1:
            neighbors.append((row + 1, col))
        if col > 0:
            neighbors.append((row, col - 1))
        if col < cols - 1:
            neighbors.append((row, col + 1))

        for neighbor in neighbors:
            nrow, ncol = neighbor
            if neighbor not in visited:
                prev[neighbor] = node
                heapq.heappush(heap, (cost + graph[nrow, ncol], neighbor))

    path = []
    current = end

    while current != start:
        path.append(current)
        current = prev[current]

    path.append(start)

    return cost, path


def paint_fastest_path(image, fastest_path):
    ret = image.copy()

    for point in fastest_path:
        row, col = point
        ret[row, col] = [0, 0, 255]

    return ret

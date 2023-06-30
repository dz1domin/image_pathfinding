import heapq
from PIL import ImageColor
import cv2
from numba import jit


@jit(nopython=True, cache=True)
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


def paint_fastest_path(image, fastest_path, color_bgr=(0, 0, 255), skip_step=1):
    ret = image.copy()
    ret = cv2.cvtColor(ret, cv2.COLOR_BGR2RGB)

    prev = fastest_path[0][1], fastest_path[0][0]
    for point in fastest_path[1::skip_step]:
        curr = point[1], point[0]
        ret = cv2.line(ret, prev, curr, color_bgr)
        prev = curr
    ret = cv2.line(ret, prev, (fastest_path[-1][1], fastest_path[-1][0]), color_bgr, lineType=cv2.LINE_AA)

    ret = cv2.cvtColor(ret, cv2.COLOR_RGB2BGR)

    return ret

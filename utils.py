import math, heapq

def tool(action_text: str):
    print(action_text)

def _dist_point_to_segment(px, py, x1, y1, x2, y2):
    """Calcula a distância de um ponto a um segmento de reta."""
    dx = x2 - x1
    dy = y2 - y1
    if dx == dy == 0:
        return math.hypot(px - x1, py - y1)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx*dx + dy*dy)
    t = max(0, min(1, t))
    projx = x1 + t * dx
    projy = y1 + t * dy
    return math.hypot(px - projx, py - projy)

def dijkstra(adjacencyList, source):
    distance = {vertex: math.inf for vertex in adjacencyList}
    previous = {vertex: None for vertex in adjacencyList}
    distance[source] = 0
    priorityQueue = [(0, source)]
    visited = set()

    while priorityQueue:
        currentDistance, currentVertex = heapq.heappop(priorityQueue)

        if currentVertex in visited:
            continue

        visited.add(currentVertex)

        for neighbourVertex, weight in adjacencyList.get(currentVertex, []):
            alternativeDistance = currentDistance + weight

            if alternativeDistance < distance[neighbourVertex]:
                distance[neighbourVertex] = alternativeDistance
                previous[neighbourVertex] = currentVertex
                heapq.heappush(priorityQueue, (alternativeDistance, neighbourVertex))

    return distance, previous
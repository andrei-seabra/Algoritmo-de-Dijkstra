import math, heapq

def tool(action_text: str):
    print(action_text)

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
import heapq

def dijkstra(graph, start, weight_type='cost'):
    distances = {node: float('inf') for node in graph}
    previous_nodes = {node: None for node in graph}
    paths = {node: [] for node in graph}
    
    distances[start] = 0
    priority_queue = [(0, start, [])]  # (cost_or_duration, current_node, path)

    while priority_queue:
        current_distance, current_node, path = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for flight in graph.get(current_node, []):
            neighbor = flight['destination']
            layover = flight['layover']
            weight = flight[weight_type]  # either cost or duration
            
            distance = current_distance + weight
            new_path = path + [ (current_node, neighbor, layover) ]

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                paths[neighbor] = new_path
                heapq.heappush(priority_queue, (distance, neighbor, new_path))

    return distances, paths

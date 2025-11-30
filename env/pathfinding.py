import heapq

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(map_obj, node):
    (x, y) = node
    neighbors = []
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x + dx, y + dy
        if not map_obj.is_wall(nx, ny):
            neighbors.append((nx, ny))
    return neighbors

def a_star_path(map_obj, start, goal):
    """
    Returns full path as list from start to goal using A*.
    If no path exists, returns None.
    """
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, start, goal)

        for neighbor in get_neighbors(map_obj, current):
            temp_g = g_score[current] + 1
            if neighbor not in g_score or temp_g < g_score[neighbor]:
                g_score[neighbor] = temp_g
                f_score = temp_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))
                came_from[neighbor] = current

    return None  # no valid path found

def reconstruct_path(came_from, start, goal):
    node = goal
    path = [node]
    while node != start:
        node = came_from[node]
        path.append(node)
    return list(reversed(path))

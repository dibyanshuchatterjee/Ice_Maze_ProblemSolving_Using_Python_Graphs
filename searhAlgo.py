"""
CSCI-603: Graphs
Author: Sean Strout @ RIT CS

This is the implementation of the three search algorithms used:
    1. canReachDFS: Can start reach end using recursive DSF (yes or no)?
    2. findPathDFS: Find any path from start to end, if one exists,
        using recursive DFS.
    3. findShortestPath:  Find the shortest path from start to end,
        if one exists, iteratively using BFS and a queue.
"""

def __canReachDFS(current, visited):
    """
    Private recursive helper function for canReachDFS.  It traverses all
    reachable nodes in the graph, recursively.
    :param current (Vertex): the current Vertex object
    :param visited (set of Vertex): the vertices already visited
    :return: None
    """
    for neighbor in current.getConnections():
        # this check prevents cycles from infinitely looping
        if neighbor not in visited:
            visited.add(neighbor)
            __canReachDFS(neighbor, visited)

def canReachDFS(start, end):
    """
    A boolean functions that indicates whether a start vertex is able
    to reach an end vertex by recursively traversing neighbors.
    :param start (Vertex): the starting vertex
    :param end (Vertex): the ending vertex
    :return: True if there is a path, False otherwise
    """
    visited = set()
    visited.add(start)
    __canReachDFS(start, visited)
    # a path exists if the end node was visited, otherwise the graph is
    # disconnected and no path exists from start to end
    return end in visited

def __findPathDFS(current, end, visited):
    """
    Private recursive helper function that finds the path, if one exists,
    from the current vertex to the end vertex
    :param current (Vertex): The current vertex in the traversal
    :param end (Vertex): The destination vertex
    :param visited (set of Vertex): the vertices already visited
    :return: A list of Vertex objects from start to end, if a path exists,
        otherwise None
    """

    # A successful base case is when we traverse to the end vertex.  In this
    # case, wrap it in a list and return it to the caller to construct the
    # full path
    if current == end:
        return [current]
    for neighbor in current.getConnections():
        if neighbor not in visited:
            visited.add(neighbor)
            path = __findPathDFS(neighbor, end, visited)
            # If the path is not None, current is part of the solution path,
            # so add it to the front of the path list and return it
            if path != None:
                path.insert(0, current)
                return path
    # No path was found, so pass back None
    return None

def findPathDFS(start, end):
    """
    Find a path, if one exists, from a start to end vertex.
    :param start (Vertex): the start vertex
    :param end (Vertex): the destination vertex
    :return: A list of Vertex objects from start to end, if a path exists,
        otherwise None
    """
    visited = set()
    visited.add(start)
    return __findPathDFS(start, end, visited)

def findShortestPath(start, end):
    """
    Find the shortest path, if one exists, between a start and end vertex
    :param start (Vertex): the start vertex
    :param end (Vertex): the destination vertex
    :return: A list of Vertex objects from start to end, if a path exists,
        otherwise None
    """
    # Using a queue as the dispenser type will result in a breadth first
    # search
    queue = []
    queue.append(start)         # prime the queue with the start vertex

    # The predecessor dictionary maps the current Vertex object to its
    # immediate predecessor.  This collection serves as both a visited
    # construct, as well as a way to find the path
    predecessors = {}
    predecessors[start] = None  # add the start vertex with no predecessor

    # Loop until either the queue is empty, or the end vertex is encountered
    while len(queue) > 0:
        current = queue.pop(0)
        if current == end:
            break
        for neighbor in current.getConnections():
            if neighbor not in predecessors:        # if neighbor unvisited
                predecessors[neighbor] = current    # map neighbor to current
                queue.append(neighbor)              # enqueue the neighbor

    # If the end vertex is in predecessors a path was found
    if end in predecessors:
        path = []
        current = end
        while current != start:              # loop backwards from end to start
            path.insert(0, current)          # prepend current to the path list
            current = predecessors[current]  # move to the predecessor
        path.insert(0, start)
        return path
    else:
        return None
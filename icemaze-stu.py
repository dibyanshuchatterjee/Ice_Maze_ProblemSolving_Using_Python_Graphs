"""
lab 9 : CSCI 603
Author: Zubin Tobias
Author: Dibyanshu Chatterjee
"""
import sys
from graph import Graph
from searhAlgo import *


class Icemaze:
    """
    An simulation of ice maze with rocks and one escape point.

    :slots: graph:  The identifier for the Graph implementation.
    :slots: rock:  A string identifier for the '*' symbol
    :slots: ice:   A string identifier for the '.' symbol
    :slots: row:   To keep a count of row
    :slots: coloumn:  To keep a count of coloumn
    :slots: escape:    The escaping row
    :slots: list:       A list to simulate a 2-D array
    :slots: gate:       Exit vertex for each traversal
        the neighbor (Vertex), and the value is the edge cost (int)
    """
    __slots__ = "graph", "rock", "ice", "row", "coloumn", "escape", "list", "gate"

    def __init__(self):
        """
        Initialize the class
        :param ice: The identifier for ice symbolisation
        :param rock:  The identifier for rock symbolisation
        :param graph: identifier to initialize graph
        :param graph:  list to simulate a 2-D array
        :return: None
        """
        self.ice = "."
        self.rock = "*"
        self.graph = Graph()
        self.list = []
        if len(sys.argv) == 2:
            with open(sys.argv[1]) as newFile:
                firstLine = newFile.readline()
                self.row = int(firstLine[0])
                self.coloumn = int(firstLine[2])
                self.escape = int(firstLine[4])
                content = newFile.read()
                result = []
                for i in content.split():
                    result.append(i)
                start = 0
                end = self.coloumn
                for i in range(self.row):
                    self.list.append(result[start:end])
                    start += self.coloumn
                    end += self.coloumn
        for y in range(self.row):
            for x in range(self.coloumn):
                if self.list[y][x] == "*":
                    continue
                else:
                    vert = self.graph.addVertex((x, y)) if self.graph.getVertex(
                        (x, y)) is None else self.graph.getVertex((x, y))
                counter = y
                while 0 <= counter < self.row and self.list[counter][x] == '.':
                    counter += 1
                if counter - 1 >= 0 and (x, counter - 1) != (x, y):
                    self.graph.addEdge(vert.id, (x, counter - 1))
                counter = y
                while 0 <= counter < self.row and self.list[counter][x] == '.':
                    counter -= 1
                if counter + 1 >= 0 and (x, counter + 1) != (x, y):
                    self.graph.addEdge(vert.id, (x, counter + 1))
                counter = x
                while 0 <= counter < self.row and self.list[y][counter] == '.':
                    counter += 1
                if counter - 1 >= 0 and (counter - 1, y) != (x, y):
                    self.graph.addEdge(vert.id, (counter - 1, y))
                counter = x
                while 0 <= counter < self.row and self.list[y][counter] == '.':
                    counter -= 1
                if counter + 1 >= 0 and (counter + 1, y) != (x, y):
                    self.graph.addEdge(vert.id, (counter + 1, y))
        dictS = dict()
        noPath = []
        for y in range(self.row):
            for x in range(self.coloumn):
                if (x, y) in self.graph.getVertices():
                    leng = findShortestPath(self.graph.getVertex((x, y)),
                                            self.graph.getVertex((self.row - 1, self.escape)))
                    if leng is None:
                        noPath.append((x, y))
                        continue
                    l = len(leng) - 1
                    if l <= 0:
                        l = 1
                    if dictS.get(str(l)) is not None:
                        dictS.get(str(l)).append((x, y))
                    else:
                        dictS[str(l)] = [(x, y)]
        for key, value in sorted(dictS.items()):
            print(key, ':', value)
        print("No path:", noPath)

    def put_in_graph(self):
        """
        Puts the vertices in the graph
        :param: None
        :return: None
        """

        flag = False

        self.add_initial_vertex()

        for j in range(self.row):
            if self.list[j].__contains__(self.rock):
                flag = True
            for i in range(self.coloumn):
                if self.list[j][i] == self.rock:
                    if i != 1:
                        for k in range(0, i - 1):
                            self.graph.addEdge((j, k), (j, (i - 1)))
                        for m in range(i, self.coloumn - 1):
                            self.graph.addEdge((j, m),
                                               (j, (self.coloumn - 1)))
                    else:
                        self.graph.addEdge((j, 0), (j, 0))
                        for m in range(2, self.coloumn - 1):
                            self.graph.addEdge((j, m),
                                               (j, (self.coloumn - 1)))
                elif (i != self.coloumn - 1) and (flag is False):
                    self.graph.addEdge((j, i), (j, (self.coloumn - 1)))
            flag = False

        for j in range(self.row):
            if self.list[j].__contains__(self.rock):
                flag = True
            for i in range(self.coloumn):
                if self.list[j][i] == self.rock:
                    if i != 0:
                        for k1 in range(1, i):
                            self.graph.addEdge((j, k1), (j, 0))
                        for m1 in range(i, self.coloumn):
                            self.graph.addEdge((j, m1),
                                               (j, i + 1))
                    else:
                        for m1 in range(1, self.coloumn):
                            self.graph.addEdge((j, m1),
                                               (j, 1))
                elif (i != self.coloumn - 1) and (flag is False):
                    for i1 in range(self.coloumn):
                        self.graph.addEdge((j, i1), (j, 0))
            flag = False

        for i in range(self.coloumn):
            for j in range(self.row):
                if self.list[j][i].__contains__(self.rock):
                    flag = True
            for j in range(self.row):
                if self.list[j][i] == self.rock:
                    if j != 1:
                        for k1 in range(0, j - 1):
                            self.graph.addEdge((k1, i), ((j - 1), i))
                        for m1 in range(j, self.row - 1):
                            self.graph.addEdge((m1, i),
                                               ((self.row - 1), i))
                    else:
                        self.graph.addEdge((0, i), (0, i))
                        for m in range(2, self.row - 1):
                            self.graph.addEdge((m, i),
                                               ((self.row - 1), i))
                elif flag is False:
                    for j1 in range(self.row):
                        self.graph.addEdge((j1, i),
                                           ((self.row - 1), i))
            flag = False

        for i in range(self.coloumn):
            for j in range(self.row):
                if self.list[j][i].__contains__(self.rock):
                    flag = True
            for j in range(self.row):
                if self.list[j][i] == self.rock:
                    if j != 0:
                        for k1 in range(1, j):
                            self.graph.addEdge((k1, i), (0, i))
                        for m1 in range(j, self.row):
                            self.graph.addEdge((m1, i),
                                               ((j + 1), i))
                    else:
                        for m1 in range(1, self.row):
                            self.graph.addEdge((m1, i),
                                               (1, i))
                elif flag is False:
                    for j1 in range(self.row):
                        self.graph.addEdge((j1, i),
                                           (0, i))
            flag = False

    def add_initial_vertex(self):
        """
        Initializes the first vertex
        :param: None
        :return: None
        """
        for i in range(self.coloumn):
            for j in range(self.row):
                if self.list[i][j] != self.rock:
                    coordinate = str(i) + str(j)
                    self.graph.addVertex(coordinate)


def main():
    Icemaze()


if __name__ == '__main__':
    main()

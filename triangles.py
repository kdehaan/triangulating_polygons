import csv
import os
import sys

DEFAULT_GRAPH = "default.csv"
DEFAULT_TYPES = {'a', 'b', 'c'}

class Vertex:
    """A point in an undirected graph"""

    key = ""
    value = None 
    neighbours = set()

    def __init__(self, key, value, neighbours):
        self.key = key
        # https://docs.python.org/3/library/csv.html#csv.writer "None is written as the empty string"
        self.value = None if value is "" else value 
        self.neighbours = set(neighbours.strip("[]").split(","))

    def getEdgeNeighbours(self, edges):
        return self.neighbours.intersection(edges)


class UndirectedGraph:
    """An undirected graph"""

    points = []
    edges = set()
    interior = set()
    edgePairs = dict() # key: type, value: set of pairs

    def __init__(self, points, edges, interior):
        if edges.union(interior) != set(points):
            raise ValueError("Graph edges and interior are incomplete")
        self.points = points
        self.edges = edges
        self.interior = interior


    def colourMinTriangles(self):
        self.sandwichEdges()
        self.findEdgePairs()
        # self.colourInterior()

        return self.points

    
    def sandwichEdges(self):
        """Finds 'sandwiches' in the edge which can be used to 'destroy' paired edges"""

        edgeValues = []
        

        prevPoint = None
        currentPoint = next(iter(self.edges)) # grab arbitrary set element
        prevPoint = next(iter(self.points[currentPoint].neighbours.intersection(self.edges)))
        startPoint = currentPoint
        
        recentEdgePair = (self.points[prevPoint].value, self.points[currentPoint].value)

        while True:
            print(currentPoint)
            edgeValues.append(self.points[currentPoint].value)
            neighbours = self.points[currentPoint].neighbours.intersection(self.edges)
            tempPoint = currentPoint
            currentPoint = next(iter(neighbours - {prevPoint}))
            prevPoint = tempPoint
            

            if currentPoint == startPoint:
                break
        

        print(edgeValues)



    def findEdgePairs(self):
        """Finds unique edge pairs. 
        Note: non-deterministic if multiple solutions are possible due to set operations
        """
        
        # at this point I messed around with intelligently reading every other 
        # point so as to minimize set operations, but I realized it only made it O(n/2) 
        # from O(n) and decided it was more trouble that it was worth

        for point in self.edges:
            edgeNeighbours = self.points[point].getEdgeNeighbours(self.edges)
            for neighbour in edgeNeighbours:
                if (self.points[neighbour].value == self.points[point].value):
                    continue
                pairType = getPairKey(self.points[neighbour].value, self.points[point].value)

                if (pairType in self.edgePairs and type(self.edgePairs[pairType]) is set):
                    self.edgePairs[pairType].add(getPairKey(point, neighbour))
                else:
                    self.edgePairs[pairType] = set([getPairKey(point, neighbour)])



def readCSV(fileLocation=DEFAULT_GRAPH):
    """Opens a .csv describing a certain polygon. Defaults to the provided example.
    Assumes that points will be labeled as a, b and c only.
    """

    points = {}
    edgePoints = set()
    interiorPoints = set()
 

    with open(fileLocation, newline='') as graphFile:
        graphReader = csv.reader(graphFile, delimiter=",")

        next(graphReader, None) # skips csv header
        for row in graphReader:
            point = Vertex(row[0], row[1], row[2])
            points[point.key] = point
            if point.value is not None:
                edgePoints.add(point.key)
            else:
                interiorPoints.add(point.key)
    graph = UndirectedGraph(points, edgePoints, interiorPoints)
        
    return graph
        

# def updateEdgePair(pair, newVal):
#     """Updates the edge pair and determines if a sandwich has been found"""

#     if newVal == pair[1]:
#         return pair, False
#     if newVal == pair[0]:
#         pair[1] = newVal
#         return pair, True
    
#     pair = swapTuple(pair)
#     pair[1] = newVal
#     return pair, False


def swapTuple(t):
    """Swaps tuple elements"""
    temp = t[0]
    t[0] = t[1]
    t[1] = temp
    return t

def getPairKey(a, b):
    """Makes sure pairs like (1, 2) and (2, 1) aren't duplicated in sets""" 

    return "({})".format(" ".join(sorted((a, b))))


def getMinTriangles(edgePairs, valueTypes):
    """Determines the unique pair type with the fewest occurrences. 
    Non-deterministic if multiple solutions are possible
    """

    minVal = float('inf')
    minPair = None
    for pair in edgePairs:
        if len(edgePairs[pair]) < minVal:
            minVal = len(edgePairs[pair])
            minPair = pair
   
    fillType = (valueTypes - set(minPair.strip("()").split(" "))).pop()
    return minVal, fillType


def main():
    fileLoc = DEFAULT_GRAPH
    if len(sys.argv) > 1:
        fileLoc = sys.argv[1]
    graph = readCSV(fileLocation=fileLoc)
    minTriangles = graph.colourMinTriangles()
    # graphPoints = sandwichEdges(graphPoints, edgePoints, interiorPoints)
    # edgePairs = findEdgePairs(graphPoints, edgePoints)
    # minTriangles, fillType = getMinTriangles(edgePairs, DEFAULT_TYPES)

#     print("The minimum number of completed triangles possible in this polygon is {}.\n\
# One way to accomplish this is to fill all empty points with the value '{}'".format(minTriangles, fillType))

    







if __name__ == "__main__":
    main()
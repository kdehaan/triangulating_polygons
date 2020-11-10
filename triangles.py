import csv
import os

DEFAULT_GRAPH = "default.csv"

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
      

    def addNeighbour(self, point):
        self.neighbours.add(point)

    def getEdgeNeighbours(self, edges):
        return self.neighbours.intersection(edges)



def readCSV(fileLocation=DEFAULT_GRAPH):
    points = {}
    edgePoints = set()

    with open(fileLocation, newline='') as graphFile:
        graphReader = csv.reader(graphFile, delimiter=",")

        next(graphReader, None) # skips csv header
        for row in graphReader:
            point = Vertex(row[0], row[1], row[2])
            points[point.key] = point
            if point.value is not None:
                edgePoints.add(point.key)
        return points, edgePoints



def findMinPairs(graph, edges):
    edgePairs = dict() # key: type, value: set of pairs

    # currentKey = next(iter(edges)) # get arbitrary point from the edge set
    
    # at this point I messed around with intelligently reading every other 
    # point so as to minimize reads, but I realized it only made it O(n/2) 
    # from O(n) and decided it was more trouble that it was worth

    for point in edges:
        edgeNeighbours = graph[point].getEdgeNeighbours(edges)
        for neighbour in edgeNeighbours:
            pairType = getPairType(graph[neighbour], graph[point])

        if (pairType in edgePairs and type(edgePairs[pairType]) is set):
            edgePairs[pairType].add(getPairKey(point, neighbour))
        else:
            edgePairs[pairType] = set([getPairKey(point, neighbour)])
    
    print(edgePairs)
    # while True:


    #     print(pairPartners)
    #     print(currentKey, chosenPartner, unchosenPartner)
    #     print(edgePairs)
    #     print("diff", pairPartners.difference(set(unchosenPartner)))

    #     break


    # print(currentKey)
    # print(pairPartners)
    

def getPairType(pointA, pointB):
    return getPairKey(pointA.value, pointB.value)

def getPairKey(a, b):
    return "({})".format(" ".join(sorted((a, b))))

def main():
    graphPoints, edgePoints = readCSV()
    findMinPairs(graphPoints, edgePoints)
    # for key in graphPoints:
    #     point = graphPoints[key]
    #     print(point.key, point.value, point.neighbours, point.isEdge)








if __name__ == "__main__":
    main()
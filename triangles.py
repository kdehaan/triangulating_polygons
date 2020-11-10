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
        self.value = value
        self.neighbours = set(neighbours.strip("[]").split(","))

    def addNeighbour(self, point):
        self.neighbours.add(point)



def readCSV(fileLocation=DEFAULT_GRAPH):
    points = {}

    with open(fileLocation, newline='') as graphFile:
        graphReader = csv.reader(graphFile, delimiter=",")

        next(graphReader, None) #skips csv header
        for row in graphReader:
            point = Vertex(row[0], row[1], row[2])
            points[point.key] = point
        return points



def main():
    graphPoints = readCSV()
 
    for key in graphPoints:
        point = graphPoints[key]
        print(point.key, point.value, point.neighbours)








if __name__ == "__main__":
    main()
import csv
import os

DEFAULT_GRAPH = "default.csv"

class Vertex:
    """A point in an undirected graph"""
    key = ""
    value = None
    neighbours = []

    def __init__(self, key):
        self.key = key

    def addNeighbour(self, point):
        self.neighbours.append(point)




def readCSV(fileLocation=DEFAULT_GRAPH):
    with open(fileLocation, newline='') as graphFile:
        graphReader = csv.reader(graphFile, delimiter=",")
        for row in graphReader:
            print(row)



def main():
    readCSV()










if __name__ == "__main__":
    main()
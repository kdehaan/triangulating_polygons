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

    def getborderNeighbours(self, borders):
        return self.neighbours.intersection(borders)


class UndirectedGraph:
    """An undirected graph"""

    points = []
    borders = set()
    interior = set()
    borderPairs = dict() # key: type, value: set of pairs

    def __init__(self, points, borders, interior):
        if borders.union(interior) != set(points):
            raise ValueError("Graph borders and interior are incomplete")
        self.points = points
        self.borders = borders
        self.interior = interior


    def colourMinTriangles(self):
        self.palindromeBorders()
        self.findBorderPairs()
        # self.colourInterior()

        return self.points

    
    def palindromeBorders(self):
        """Finds palindromes in the border which can be used to 'destroy' paired borders"""

        borderNodes = []
        

        prevPoint = None
        currentPoint = next(iter(self.borders)) # grab arbitrary set element
        prevPoint = next(iter(self.points[currentPoint].getborderNeighbours(self.borders)))
        startPoint = currentPoint
        

        while True:
            borderNodes.append({"value": self.points[currentPoint].value, "key": self.points[currentPoint].key})
            neighbours = self.points[currentPoint].neighbours.intersection(self.borders)
            tempPoint = currentPoint
            currentPoint = next(iter(neighbours - {prevPoint}))
            prevPoint = tempPoint
            
            if currentPoint == startPoint:
                break
        
        self.trimBorders(borderNodes)
        


    def trimBorders(self, borderNodes):
        """Finds and trims palindromic sublists.
        Based off of https://www.tutorialspoint.com/palindromic-substrings-in-python
        """

        # print(borderNodes)
        palindromes = []
        borderValues = [x['value'] for x in borderNodes]
        borderKeys = [x['key'] for x in borderNodes]
        # print(borderNodes, borderValues)
        print("values", borderValues)
        print("keys  ", borderKeys)
        for startIdx in range(len(borderValues)):
            for endIdx in range(startIdx+1, len(borderValues)+1):
                temp = borderValues[startIdx:endIdx]
                if len(temp) > 1 and temp == temp [::-1]:
                    if (len(set(temp)) == 2):
                        palindromes.append((startIdx, endIdx-1))
                        print("palindrome: ", temp)

        print(palindromes)






    def findBorderPairs(self):
        """Finds unique border pairs. 
        Note: non-deterministic if multiple solutions are possible due to set operations
        """
        
        # at this point I messed around with intelligently reading every other 
        # point so as to minimize set operations, but I realized it only made it O(n/2) 
        # from O(n) and decided it was more trouble that it was worth

        for point in self.borders:
            borderNeighbours = self.points[point].getborderNeighbours(self.borders)
            for neighbour in borderNeighbours:
                if (self.points[neighbour].value == self.points[point].value):
                    continue
                pairType = getPairKey(self.points[neighbour].value, self.points[point].value)

                if (pairType in self.borderPairs and type(self.borderPairs[pairType]) is set):
                    self.borderPairs[pairType].add(getPairKey(point, neighbour))
                else:
                    self.borderPairs[pairType] = set([getPairKey(point, neighbour)])



def readCSV(fileLocation=DEFAULT_GRAPH):
    """Opens a .csv describing a certain polygon. Defaults to the provided example.
    Assumes that points will be labeled as a, b and c only.
    """

    points = {}
    borderPoints = set()
    interiorPoints = set()
 

    with open(fileLocation, newline='') as graphFile:
        graphReader = csv.reader(graphFile, delimiter=",")

        next(graphReader, None) # skips csv header
        for row in graphReader:
            point = Vertex(row[0], row[1], row[2])
            points[point.key] = point
            if point.value is not None:
                borderPoints.add(point.key)
            else:
                interiorPoints.add(point.key)
    graph = UndirectedGraph(points, borderPoints, interiorPoints)
        
    return graph
        

# def updateborderPair(pair, newVal):
#     """Updates the border pair and determines if a palindrome has been found"""

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


def getMinTriangles(borderPairs, valueTypes):
    """Determines the unique pair type with the fewest occurrences. 
    Non-deterministic if multiple solutions are possible
    """

    minVal = float('inf')
    minPair = None
    for pair in borderPairs:
        if len(borderPairs[pair]) < minVal:
            minVal = len(borderPairs[pair])
            minPair = pair
   
    fillType = (valueTypes - set(minPair.strip("()").split(" "))).pop()
    return minVal, fillType


def main():
    fileLoc = DEFAULT_GRAPH
    if len(sys.argv) > 1:
        fileLoc = sys.argv[1]
    graph = readCSV(fileLocation=fileLoc)
    minTriangles = graph.colourMinTriangles()
    # graphPoints = palindromeborders(graphPoints, borderPoints, interiorPoints)
    # borderPairs = findborderPairs(graphPoints, borderPoints)
    # minTriangles, fillType = getMinTriangles(borderPairs, DEFAULT_TYPES)

#     print("The minimum number of completed triangles possible in this polygon is {}.\n\
# One way to accomplish this is to fill all empty points with the value '{}'".format(minTriangles, fillType))

    







if __name__ == "__main__":
    main()
import csv
import os
import sys


DEFAULT_GRAPH = "sample5.csv"
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

    types = DEFAULT_TYPES
    points = []
    borders = set()
    interior = set()
    # obsolete = set()
    borderPairs = dict() # key: type, value: set of pairs

    def __init__(self, points, borders, interior):
        if borders.union(interior) != set(points):
            raise ValueError("Graph borders and interior are incomplete")
        self.points = points
        self.borders = borders
        self.interior = interior


    def getNeighbours(self, point):
        """Retrieves the active neighbours of a vertex"""

        neighbours = set()
        for neighbour in self.points[point].neighbours:
            if neighbour in self.borders or neighbour in self.interior:
                neighbours.add(neighbour)
        return neighbours


    def safeToColour(self, pointKey, pointValue):
        """Checks if colouring this point a given colour will complete a triangle"""

        neighbours = self.getNeighbours(pointKey)
        nearTypes = set([self.points[x].value for x in neighbours])
        if None in nearTypes:
            nearTypes.remove(None)
        if pointValue in nearTypes: # we don't care about nearby points that are the same as we want to colour
            nearTypes.remove(pointValue)
        if len(nearTypes) < 2:
            return True


        # this isn't as bad as it looks, I promise

        for point in neighbours: # for each neighbour
            if self.points[point].value in nearTypes: # if they have a potentially risky colour
                for subPoint in self.getNeighbours(point): #for each of those neighbours
                    if (self.points[subPoint].value is not self.points[point].value  # if they have a different colour
                    and self.points[subPoint].value in nearTypes # which is the other risky colour
                    and pointKey in self.getNeighbours(subPoint)): # and it's also a neighbour of the original point
                        return False # ...then it isn't safe to colour.

        return True # ...otherwise, it is


    def colourMinTriangles(self):
        self.trimBorders()
        self.findBorderPairs()
        # self.colourInterior()

        return self.points

    

    def trimBorders(self):
        """Attempts to use palindromes to 'destroy' paired borders"""
        
        while True: #reducing palindromes can produce more palindromes, so iterate until they're all gone

            borderNodes = self.getBorderPath()
            print("border:", borderNodes)

            palindromes = findPalindromes(borderNodes)
            if (len(palindromes) == 0):
                print("no palindromes found")
                break

            # this is guaranteed to converge because there are a limited number of palindromes possible
            noValidPalindromesLeft = True
            for idx in palindromes:
                sequence = self.getPalindromeSequence(idx, palindromes[idx], borderNodes)
                print("sequence", sequence)
                if not sequence:
                    continue
                valid = self.coverPalindrome(sequence)
                if valid:
                    print("valid found")
                    noValidPalindromesLeft = False

            if noValidPalindromesLeft:
                break
      


    def getBorderPath(self):
        """Uses recursive backtracking to find the circumference (maximal cycle) of the graph's border
        The circumference is necessary due to the possibility of holes in the graph
        This problem is NP-hard, hence recursive backtracking
        """
   
        paths = []
        startPoint = next(iter(self.borders)) # grab arbitrary set element
    
        prevPoint = next(iter(self.points[startPoint].getborderNeighbours(self.borders))) # grab arbitrary direction to be backwards
        currentPoint = startPoint

        path = [prevPoint]
        checked = {None} # hack to get rid of strings misbehaving
        possibleRoutes = []

        checked.add(currentPoint)
        path.append(currentPoint)
        possibleRoutes.append(self.getOtherBorderNodes(currentPoint, path[-2]))
        print("startpoint", startPoint, "prevpoint", prevPoint)
        # if (startPoint == 11 and ((prevPoint == 1) or (prevPoint == 10))):
        #     print("stop")
        print("possibleRoutes", possibleRoutes)

        while len(path) > 1:
            
            if len(possibleRoutes[-1]) > 0:
                nextNode = possibleRoutes[-1].pop()
                if (nextNode == startPoint):
                    paths.append(path[:-1].copy()) # copy the state, not the reference
        
                if (nextNode not in checked):
                    currentPoint = nextNode
                    checked.add(currentPoint)
                    path.append(currentPoint)
                    possibleRoutes.append(self.getOtherBorderNodes(currentPoint, path[-2]))
                    continue
        
            checked.remove(currentPoint)
            path.pop()
            possibleRoutes.pop()
            currentPoint = path[-1]

        if len(paths) == 0:
            print('what')
        pathLengths = [len(x) for x in paths]
        print("paths", paths, "pathLengths", pathLengths)
        longestPath = paths[pathLengths.index(max(pathLengths))]
   
        borderNodes = [{"value": self.points[x].value, "key":x} for x in longestPath]
        
        return borderNodes
        

    def getOtherBorderNodes(self, key, prev):
        """Given a key and one of it's border neighbours, returns the other border neighbour"""

        if key in self.borders:
            neighbours = self.points[key].getborderNeighbours(self.borders)
            return neighbours - {prev}
        else:
            raise ValueError("Vertex is not on the border")



    def coverPalindrome(self, sequence):
        """Attempts to 'cover' a palindrome to eliminate a paired edge
        Returns True on success, False on failure
        """

        coverValue = self.points[sequence[0]].value # the value of the 'border' of the palindrome, used to 'cover' the rest

        palindromeCore = sequence[1:-1]

        if not set(sequence).issubset(self.borders): # palindrome is obsolete, abort
            return False
        
        print("got ", self.getNeighbours(palindromeCore[0]))
        print("coreNeighbours", [self.getNeighbours(key) for key in palindromeCore])
        print("coreNeighbours2", [self.points[key].neighbours for key in palindromeCore])

        allNeighbours = set().union(*[self.getNeighbours(key) for key in palindromeCore]) # finding candidates to 'cover'

        print("allNeighbours", allNeighbours)

        interiorNeighbours = allNeighbours - self.borders # set difference s-t is O(len(s)) in python
        # so this is better than allNeighbours ∩ self.interior, which would be worst case O(len(s)*len(t))
        # https://wiki.python.org/moin/TimeComplexity

        isSafe = True
        for point in interiorNeighbours:
            if not self.safeToColour(point, coverValue):
                isSafe = False
        
        if isSafe:
            for point in interiorNeighbours:
                self.points[point].value = coverValue # this is where the colours are actually changed
                print("point", point, "is now ", coverValue)

            self.borders = self.borders.union(interiorNeighbours)

            # sometimes the outer points of the sequence can be covered, if so, remove from the border
            for point in [sequence[0], sequence[-1]]:
                stillBorder = False
                for neighbour in self.getNeighbours(point):
                    if neighbour not in self.borders:
                        stillBorder = True
                if not stillBorder:
                    self.borders.remove(point)
                    print("removing", point)
            
            self.borders = self.borders - set(palindromeCore) # update borders
            self.interior = self.interior - interiorNeighbours
            return True

        return False
 
        

    def getPalindromeSequence(self, idx, size, nodes):
        """Finds the largest interior palindrome of exactly two value types"""

        sequence = []
        leftOffset = rightOffset = 1
        sequence = [idxToKey(idx-leftOffset, nodes), idxToKey(idx, nodes), idxToKey(idx+rightOffset, nodes)]
        if idx % 1:
            rightOffset += 1
            sequence.append(idxToKey(idx+rightOffset, nodes)) # handles even palindromes

        pointValues = [self.points[x].value for x in sequence]

        while len(set(pointValues)) < 2:
            leftOffset += 1
            rightOffset += 1
            sequence.insert(0, idxToKey(idx-leftOffset, nodes))
            sequence.append(idxToKey(idx+rightOffset, nodes))
            pointValues = [self.points[key].value for key in sequence]

            print("size", leftOffset + rightOffset + 1)
            if ((leftOffset + rightOffset + 1) > size): # max palindrome contains only one value
                return None
        return sequence


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


def idxToKey(idx, nodes):
    """Retrieves the vertex key corresponding to the index"""
    numNodes = len(nodes)
    return nodes[int(idx)%numNodes]['key']

def findPalindromes(borderNodes):
        """Finds palindromic sublists in O(n).
        Based off of Manacher's Algorithm (linear time palindromes)
        https://leetcode.com/problems/longest-palindromic-substring/discuss/3337/Manacher-algorithm-in-Python-O(n)
        """

        palindromes = {}
        borderValues = [x['value'] for x in borderNodes]
        borderKeys = [x['key'] for x in borderNodes]
        print("values", borderValues)
        print("keys  ", borderKeys)

        valuesString = '#'.join('^{}$' # buffered to track string start/end for Manacher's
        .format("".join(borderValues) + "".join(borderValues))) # duplicated to account for wrapped palindromes
            
        # Find palindromes
        n = len(valuesString)
        p = [0]*n
        c = r = 0
        for idx in range(1, n-1):
            p[idx] = (r > idx) and min(r - idx, p[2*c - idx])
            while valuesString[idx + 1 + p[idx]] == valuesString[idx - 1 - p[idx]]:
                p[idx] += 1
            if idx + p[idx] < r:
                c, r = idx, idx + p[idx]

     
        # Account for wrapped substrings and format the index (even palindromes will have x.5 indices)
        for i in range(0, len(p)):
            if p[i] >= 3: # filter out size 1 and 2, guaranteed to be a single value type
                idx = i/2 -1
                size = p[i]
                if (idx - size/2) < len(borderValues):
                    idx = idx % len(borderValues) 
                    palindromes[idx] = p[i]
                 
        return palindromes



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
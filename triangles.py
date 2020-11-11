import csv
import os
import sys
import argparse

DEFAULT_GRAPH = "default.csv"
DEFAULT_TYPES = {'a', 'b', 'c'}


class Vertex:
    """A point in an undirected graph"""

    key = ""
    value = None
    neighbours = set()

    def __init__(self, key, value, neighbours):
        self.key = key
        # https://docs.python.org/3/library/csv.html#csv.writer
        # "None is written as the empty string"
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

    borderPairs = dict()  # key: type, value: set of pairs

    def __init__(self, points, borders, interior):
        if borders.union(interior) != set(points):
            raise ValueError("Graph borders and interior are incomplete")
        self.points = points
        self.borders = borders
        self.interior = interior

    def colourMinTriangles(self, fileOut=None):
        self.trimBorders()
        self.findBorderPairs()
        # pairs = self.findBorderPairs()
        minTriangles, fillType = self.getMinTriangles()
        print("A minimum of {} completed triangles is possible by filling \
any remaining points with {}.\nThere may be multiple valid solutions."""
              .format(minTriangles, fillType))

        if (fileOut):
            self.fillEmpty(fillType)
            with open(fileOut, 'w', newline='') as csvFile:
                graphWriter = csv.writer(csvFile, delimiter=",",
                                         quotechar='"')
                graphWriter.writerow(['key', 'value', 'neighbours'])
                for point in self.points:
                    vertex = self.points[point]
                    graphWriter.writerow([vertex.key, vertex.value,
                                         list([int(i)
                                              for i in vertex.neighbours])])

        return minTriangles, fillType

    def getNeighbours(self, point):
        """Retrieves the active neighbours of a vertex"""

        neighbours = set()
        for neighbour in self.points[point].neighbours:
            if neighbour in self.borders or neighbour in self.interior:
                neighbours.add(neighbour)
        return neighbours

    def safeToColour(self, pointKey, pointValue):
        """Checks if colouring this point a given colour
        will complete a triangle
        """

        neighbours = self.getNeighbours(pointKey)
        nearTypes = set([self.points[x].value for x in neighbours])
        if None in nearTypes:
            nearTypes.remove(None)

        # we don't care about nearby points that
        # are the same as we want to colour
        if pointValue in nearTypes:
            nearTypes.remove(pointValue)
        if len(nearTypes) < 2:
            return True

        # this isn't as bad as it looks, I promise

        # for each neighbour
        for point in neighbours:
            # if they have a potentially risky colour
            if self.points[point].value in nearTypes:
                # for each of those neighbours
                for subPoint in self.getNeighbours(point):
                    # if they have a different colour
                    if (self.points[subPoint].value
                            is not self.points[point].value
                            # which is the other risky colour
                            and self.points[subPoint].value in nearTypes
                            # and it's also a neighbour of the original point
                            and pointKey in self.getNeighbours(subPoint)):
                        return False  # ...then it isn't safe to colour...

        return True  # ...otherwise, it is

    def fillEmpty(self, fillValue):
        """Fills in empty points in O(n) time"""

        for point in self.points:
            if self.points[point].value is None:
                self.points[point].value = fillValue

    def trimBorders(self):
        """Attempts to use palindromes to 'destroy' paired borders"""

        # reducing palindromes can produce more palindromes,
        # so iterate until they're all gone
        while True:

            borderNodes = self.getBorderPath()

            palindromes = findPalindromes(borderNodes)
            if (len(palindromes) == 0):
                break

            # this is guaranteed to converge because
            # there are a limited number of palindromes possible
            noValidPalindromesLeft = True
            for idx in palindromes:
                sequence = self.getPalindromeSequence(idx,
                                                      palindromes[idx],
                                                      borderNodes)
                if not sequence:
                    continue
                valid = self.coverPalindrome(sequence)

                if valid:
                    noValidPalindromesLeft = False

            if noValidPalindromesLeft:
                break

    def getBorderPath(self):
        """Uses recursive backtracking to find the circumference
        (maximal cycle) of the graph's border. The circumference
        is necessary due to the possibility of holes in the graph
        This problem is NP-hard, hence recursive backtracking
        """

        paths = []
        startPoint = next(iter(self.borders))  # grab arbitrary set element

        # grab arbitrary direction to be backwards
        prevPoint = next(iter(self.points[startPoint]
                         .getborderNeighbours(self.borders)))
        currentPoint = startPoint

        path = [prevPoint]
        checked = {None}  # hack to get rid of strings misbehaving
        possibleRoutes = []

        checked.add(currentPoint)
        path.append(currentPoint)
        possibleRoutes.append(self.getOtherBorderNodes(currentPoint, path[-2]))

        while len(path) > 1:

            if len(possibleRoutes[-1]) > 0:
                nextNode = possibleRoutes[-1].pop()
                if (nextNode == startPoint):
                    # copy the state, not the reference
                    paths.append(path[:-1].copy())

                if (nextNode not in checked):
                    currentPoint = nextNode
                    checked.add(currentPoint)
                    path.append(currentPoint)
                    possibleRoutes.append(self.getOtherBorderNodes(
                                          currentPoint, path[-2]))
                    continue

            checked.remove(currentPoint)
            path.pop()
            possibleRoutes.pop()
            currentPoint = path[-1]

        pathLengths = [len(x) for x in paths]
        longestPath = paths[pathLengths.index(max(pathLengths))]
        borderNodes = [{"value": self.points[x].value, "key":x}
                       for x in longestPath]

        return borderNodes

    def getOtherBorderNodes(self, key, prev):
        """Given a key and one of it's border neighbours,
        returns the other border neighbour
        """

        if key in self.borders:
            neighbours = self.points[key].getborderNeighbours(self.borders)
            return neighbours - {prev}
        else:
            raise ValueError("Vertex is not on the border")

    def coverPalindrome(self, sequence):
        """Attempts to 'cover' a palindrome to eliminate a paired edge
        Returns True on success, False on failure
        """

        # the value of the 'border' of the palindrome, used to 'cover' the rest
        coverValue = self.points[sequence[0]].value

        palindromeCore = sequence[1:-1]

        # palindrome is obsolete, abort
        if not set(sequence).issubset(self.borders):
            return False

        # finding candidates to 'cover'
        allNeighbours = set().union(*[self.getNeighbours(key)
                                      for key in palindromeCore])

        interiorNeighbours = allNeighbours - self.borders
        # set difference s-t is O(len(s)) in python
        # so this is better than allNeighbours ∩ self.interior,
        # which would be worst case O(len(s)*len(t))
        # https://wiki.python.org/moin/TimeComplexity

        isSafe = True
        for point in interiorNeighbours:
            if not self.safeToColour(point, coverValue):
                isSafe = False

        if isSafe:
            for point in interiorNeighbours:
                # this is where the colours are actually changed
                self.points[point].value = coverValue
                print("Fill point", point, "with ", coverValue)

            self.borders = self.borders.union(interiorNeighbours)

            # sometimes nodes can be 'folded' into the border.
            # If so, remove from the border
            nearByNodes = set().union(*[self.getNeighbours(key)
                                      for key in interiorNeighbours])
            atRiskNodes = (nearByNodes - interiorNeighbours) \
                - set(palindromeCore)

            for point in atRiskNodes:
                if point not in self.borders:
                    continue

                stillBorder = False
                for neighbour in self.getNeighbours(point):
                    if neighbour not in self.borders:
                        stillBorder = True
                if not stillBorder:
                    self.borders.remove(point)

            self.borders = self.borders - set(palindromeCore)  # update borders
            self.interior = self.interior - interiorNeighbours
            return True

        return False

    def getPalindromeSequence(self, idx, size, nodes):
        """Finds the largest interior palindrome of exactly two value types"""

        sequence = []
        leftOffset = rightOffset = 1
        sequence = [idxToKey(idx-leftOffset, nodes), idxToKey(idx, nodes),
                    idxToKey(idx+rightOffset, nodes)]
        if idx % 1:
            rightOffset += 1
            sequence.append(idxToKey(idx+rightOffset, nodes))
            # handles even palindromes

        pointValues = [self.points[x].value for x in sequence]

        while len(set(pointValues)) < 2:
            leftOffset += 1
            rightOffset += 1
            sequence.insert(0, idxToKey(idx-leftOffset, nodes))
            sequence.append(idxToKey(idx+rightOffset, nodes))
            pointValues = [self.points[key].value for key in sequence]

            # max palindrome contains only one value
            if ((leftOffset + rightOffset + 1) > size):
                return None
        return sequence

    def findBorderPairs(self):
        """Finds unique border pairs.
        Note: non-deterministic if multiple solutions
        are possible due to set operations
        """

        # at this point I messed around with intelligently reading every other
        # point so as to minimize set operations, but I realized it only made
        # it O(n/2) from O(n) and decided it was more trouble that it was worth

        for point in self.borders:
            borderNeighbours = self.points[point] \
                            .getborderNeighbours(self.borders)

            for neighbour in borderNeighbours:
                if (self.points[neighbour].value == self.points[point].value):
                    continue
                pairType = getPairKey(self.points[neighbour].value,
                                      self.points[point].value)

                if (pairType in self.borderPairs
                        and type(self.borderPairs[pairType]) is set):
                    self.borderPairs[pairType].add(getPairKey
                                                   (point, neighbour))
                else:
                    self.borderPairs[pairType] = set([getPairKey(
                                                     point, neighbour)])

    def getMinTriangles(self):
        """Determines the unique pair type with the fewest occurrences.
        Non-deterministic if multiple solutions are possible
        """

        minVal = float('inf')
        minPair = None
        for pair in self.borderPairs:
            if len(self.borderPairs[pair]) < minVal:
                minVal = len(self.borderPairs[pair])
                minPair = pair

        fillType = (self.types - set(minPair.strip("()").split(" "))).pop()
        return minVal, fillType


def idxToKey(idx, nodes):
    """Retrieves the vertex key corresponding to the index"""
    numNodes = len(nodes)
    return nodes[int(idx) % numNodes]['key']


def findPalindromes(borderNodes):
    """Finds palindromic sublists in O(n).
    Based off of Manacher's Algorithm (linear time palindromes)
    https://leetcode.com/problems/longest-palindromic-substring/discuss/3337/Manacher-algorithm-in-Python-O(n)
    """

    palindromes = {}
    borderValues = [x['value'] for x in borderNodes]
    borderKeys = [x['key'] for x in borderNodes]

    # buffered to track string start/end for Manacher's
    valuesString = '#'.join('^{}$'.format("".
                            join(borderValues) + "".join(borderValues)))
    # duplicated to account for wrapped palindromes

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

    # Account for wrapped substrings and format the index
    # (even palindromes will have x.5 indices)
    for i in range(0, len(p)):
        # filter out size 1 and 2, guaranteed to be a single value type
        if p[i] >= 3:
            idx = i/2 - 1
            size = p[i]
            if (idx - size/2) < len(borderValues):
                idx = idx % len(borderValues)
                palindromes[idx] = p[i]

    return palindromes


def readCSV(fileLocation=DEFAULT_GRAPH):
    """Opens a .csv describing a certain polygon.
    Defaults to the provided example.
    Assumes that points will be labeled as a, b and c only.
    """

    points = {}
    borderPoints = set()
    interiorPoints = set()

    with open(fileLocation, newline='') as graphFile:
        graphReader = csv.reader(graphFile, delimiter=",")

        next(graphReader, None)  # skips csv header
        for row in graphReader:
            point = Vertex(row[0], row[1], row[2])
            points[point.key] = point
            if point.value is not None:
                borderPoints.add(point.key)
            else:
                interiorPoints.add(point.key)
    graph = UndirectedGraph(points, borderPoints, interiorPoints)

    return graph


def swapTuple(t):
    """Swaps tuple elements"""
    temp = t[0]
    t[0] = t[1]
    t[1] = temp
    return t


def getPairKey(a, b):
    """Makes sure pairs like (1, 2) and (2, 1) aren't duplicated in sets"""

    return "({})".format(" ".join(sorted((a, b))))


def main():
    """Optional arguments:
    -f filename.csv     specify input file
    -o filename.csv     write output to filename.csv
    """
    parser = argparse.ArgumentParser(description="Triangluate some polygons.")
    parser.add_argument("-f", "--fileIn", type=str,
                        help="specify input file")
    parser.add_argument("-o", "--fileOut", type=str,
                        help="write output to given filename")

    args = parser.parse_args()
    fileLoc = DEFAULT_GRAPH
    if args.fileIn:
        fileLoc = args.fileIn
    # if len(sys.argv) > 1:
    #     fileLoc = sys.argv[1]
    graph = readCSV(fileLocation=fileLoc)
    graph.colourMinTriangles(args.fileOut)


if __name__ == "__main__":
    main()

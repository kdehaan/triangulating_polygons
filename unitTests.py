import unittest
from parameterized import parameterized
import triangles

NUM_ITER = 100

class TestGraphSamplesSequence(unittest.TestCase):
    @parameterized.expand([
        "default.csv", 
        "trivial.csv", 
        "sample1.csv", 
        "sample2.csv", 
        "sample3.csv", 
        "sample4.csv", 
        "sample5.csv", 
        "sample6.csv"
    ])
    
    def testSample(self, dataFile):
        """Runs the (non-deterministic) test NUM_ITER times and 
        confirms that the final answer is always equivalent
        """

        minTrianglesSet = set()
        for _ in range(NUM_ITER):
            graph = triangles.readCSV(fileLocation=dataFile)
            minTriangles, _ = graph.colourMinTriangles()
            minTrianglesSet.add(minTriangles)
        self.assertTrue(len(minTrianglesSet) == 1)

if __name__ == '__main__':
    unittest.main()
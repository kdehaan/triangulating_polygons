# Triangulating Polygons

# General Overview

# Timeline

# Thought Process

    Language selection:
        Python is the first language of choice due to ease of use and simplicity of execution

        Runtime is more likely to be affected by time complexity than language speed to any significant extent, so Python is appropriate to use

    First Steps:
        -Look up "polygon triangulation"
        -Try to solve by hand to see where the complexity lies
            Initial findings from hand solving:

                The number of 'complete' triangles seems to be linked to the amount of two-colour edges. In this example, the are exactly three edges with each of a-b, a-c, and b-c. My clumsy attempts at hand solving all involve at least 3 'complete' triangles.

                A naive approach of filling all the center points with the same colour results in 3 triangles every time, due to the edges noted above.

                Filling in points near edges without completing triangles in order to 'shrink' the polygon maintains the number of each edge colour pair.

                I am initially inclined to think that the colouring task is impossible, and will now look to justify this instinct.

        -Set up a way to deal with this graph (and others) in python

# Resources

https://en.wikipedia.org/wiki/Polygon_triangulation

https://github.com/Clarkew5/Triangulating-Polygons-Challenge (NOT USED, found it and deliberately ignored the contents)

# Hindsight Improvements

# Execution Instructions

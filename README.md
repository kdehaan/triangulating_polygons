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

                Thought: is this related to the four-colour problem?

                Observation (I):
                Edges between two different coloured points (henceforth 'pair edges') cannot be 'destroyed' without completing a triangle. For example, with an a-b pair, you cannot add either an 'a' or a 'b' without creating a new a-b pair, and to add a 'c' would complete a triangle. This is independent of the structure of internal triangles.

                Statement to prove:
                The minimum number of complete triangles in any such polygon is equal to the minimum existing number of pair edges among any of the possible types of paired edges in the graph.
                For example, in the given polygon there are three a-b pairs, three a-c pairs, and three b-c pairs, so three is the minimum number of completed triangles.

                Naive, informal proof by contradiction in the trivial case:
                Given a three sided polygon of a, b, and c vertices, there exists some way to add vertices inside this triangle such that n-1 (where n is the minimum pair number, or 1 in this instance) completed triangles are formed (so '0' triangles in this instance).
                Due to observation I, it is known that the pair types cannot be 'destroyed', thus guaranteeing that there is always at least one edge of each pair type. In order to fill the polygon with 0 completed triangles, the final triangle (whichever that is) must have at least two edges that are identical. This is impossible, and thus the premise is proved.

                Expanding to n-sided polygons:
                Given an n-sided polygon where the minimum pair number is p, assume there exists some colouring pattern that produces at most p-1 completed triangles. Given that the creation of an 'incomplete' triangle cannot reduce the pair number, it will remain constant until any completed triangles are formed. Therefore, to meet the condition of at most p-1 completed triangles, we must create at most p-1 triangles that collectively have at least p edges of the minimum type. Each completed triangle has, by definition, 1 of each pair type and three pairs - no more, no less. It is now apparent that p-1 triangles cannot produce p edges of any type, and will always have p-1, meaning that the polygon must have at least p completed triangles by proof of contradiction.


        -Set up a way to deal with this graph (and others) in python


        -Coming back after a break:
            I have realized that while this works on the example provided, it is not exhaustive on all polygons. While a pair edge cannot be destroyed in the example, where all of the pairs are directed the same way, a pair sandwich (or palindrome) such as a-b-a can be 'destroyed' by surrounding the 'b' with 'a's. My new approach will be to eliminate as many pair edges as possible with 'sandwiches', incrementally reducing the edge of the polygon into uniquely directed pairs, then applying the original solution on this version of the graph. This solution is guaranteed to work in the case where there are an infinite amount of triangles inside the polygon and the sandwiching will have enough space so that it doesn't interfere with other borders; however, if another edge is too close to the newly created border, the sandwiching can fail. As far as I can tell, the best approach here is to attempt to sandwich and simply not do it if it would interact with another border. I do not have the background in graph theory to fully prove that this is an optimal solution, and in truth I suspect that there will be some very specific edge cases where it will not work, but it should be correct on the vast majority of polygons (and will be 100% accurate on the example polygon).

# Resources

https://en.wikipedia.org/wiki/Polygon_triangulation (not very useful tbh)

https://github.com/Clarkew5/Triangulating-Polygons-Challenge (NOT USED, found it and deliberately ignored the contents)

# Hindsight Improvements

# Execution Instructions

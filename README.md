### Triangulating Polygons

# General Overview

    The general premise of this problem is to fill in the interior dots on a polygon comprised of triangles such that there is no more than a given number of 'completed' (that is, comprising of all three colours) triangles.

    The plain english description for how this program works is that it identifies two-value 'paired' edges, such as a-b, a-c, or b-c, and then determines if it can make them go away. In the event that a paired edge is palindromic (for example, a-b-a or c-a-a-a-a-a-c), it attempts to 'cover' the middle of the palindrome by colouring over it with the value on the extremes of the sequence. If this can be accomplished without accidentally completing a triangle, it does so. The active border of the polygon is then updated and the search for palindromes is performed again until the low hanging fruit is gone.

    From this point, the active border is analysed to determine the number of (now directed) pair edges remaining. Whenever there is at least one of each pair type remaining, it is impossible to fill the polygon without producing at least one completed triangle, regardless of the internal triangle structure. As such, each full triplet of a-b/a-c/b-c corresponds to exactly one completed triangle. By finding the minimum pair occurrence, it is then possible to directly compute the minimum number of completed triangles that can be produced. Additionally, because the palindromic edges have been eliminated wherever possible, (one of) the correct way(s) to colour the rest of the polygon is to simply fill all blank spaces with the colour _not_ in the pair of minimum occurrence (or if there are multiple minimum pairs, any color that sits out of at least one of them).

# Timeline

    (As described by git commits)

    4 hours:    Initial read-through of the problem and first attempt
    (Slept overnight)
    2 hours:    Realizing how my first attempt was incomplete, and figuring out how to deal with palindromes
    4.5 hours:  Working bugs out of the palindrome code and
    3.5 hours:  Working bugs out of the recursive backtracker
    2 hours:    Polish, minor bugs, unit tests and updating the readme

    Total: approx. 16  hours (probably give or take an hour since GitHub doesn't track breaks)

# Thought Process

    Language selection:
        - Python is the first language of choice due to ease of use and simplicity of execution
        - Runtime is more likely to be affected by time complexity than language speed to any significant extent, so Python is appropriate to use

    First Steps:
        - Look up "polygon triangulation"
        - Try to solve by hand to see where the complexity lies

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

    Coming back after a break:

        I have realized that while this works on the example provided, it is not exhaustive on all polygons. While a pair edge cannot be destroyed in the example, where all of the pairs are directed the same way, a pair sandwich (or palindrome) such as a-b-a can be 'destroyed' by surrounding the 'b' with 'a's. My new approach will be to eliminate as many pair edges as possible with 'sandwiches', incrementally reducing the edge of the polygon into uniquely directed pairs, then applying the original solution on this version of the graph. This solution is guaranteed to work in the case where there are an infinite amount of triangles inside the polygon and the sandwiching will have enough space so that it doesn't interfere with other borders; however, if another edge is too close to the newly created border, the sandwiching can fail. As far as I can tell, the best approach here is to attempt to sandwich and simply not do it if it would interact with another border. I do not have the background in graph theory to fully prove that this is an optimal solution, and in truth I suspect that there will be some very specific edge cases where it will not work, but it should be correct on the vast majority of polygons (and will be 100% accurate on the example polygon).

        Another issue of traversing the edge of the graph has risen - in order to shift the border inwards, the path of the edge must be known. This is an NP-hard problem, and as such a depth-first recursive backtracking algorithm is the best solution available (unless you would like to prove P=NP while you're at it).

# Resources

    https://en.wikipedia.org/wiki/Polygon_triangulation (not very useful tbh)

    https://github.com/Clarkew5/Triangulating-Polygons-Challenge (NOT USED, found it and deliberately ignored the contents)

    https://en.wikipedia.org/wiki/Longest_palindromic_substring

    https://leetcode.com/problems/longest-palindromic-substring/discuss/3337/Manacher-algorithm-in-Python-O(n)

    https://perso.limsi.fr/pointal/_media/python:cours:mementopython3-english.pdf

    The Official Python docs

    Various Stack Overflow posts for things like how to increment a CSVwriter

    I went back to check out how I implemented recursive backtracking in my intro computing course https://github.com/kdehaan/ArduinoMazeAlgorithms/blob/master/maze.cpp

# Hindsight Improvements

    The most likely source of improvement would be to flesh out the test cases in order to determine if there are any more edge cases missing. Overall, I'm happy will my code structure, although I will comment that in a professional environment I would be incline to make better use of modules; I kept the majority of the functional code in one .py file to facilitate reading (and ctrl-f) without requiring a comprehensive IDE setup.

    Another possible improvement would be to alter the palindrome-finding code such that it is able to short-circuit when a given palindrome has only one value inside; I'm still handling this case, but the speed (_not_ the time complexity) of the program would likely be improved if the final passthrough could be skipped.

    Other things that this solution is missing, which I would add if I were to spend more time on it:
        - Determining if 'up to' a given amount of triangles is possible is left as an exercise for the reader. In most cases this is trivial.
        - The proof is not rigorous in the general case. While I am fairly confident in my analysis, it not unlikely that I have overlooked an edge case, simply because I do not have the required background in graph theory. (Or because I just missed it :slightly_smiling_face:)
        - This solution is not guaranteed to work on polygons with holes, or non-planar polygons.
            (it might work for some of them, though)

    Some examples of unit tests that I would add:
        - Specific

# Execution Instructions

    Download or clone the repository to the folder of your choice. From inside the folder, on a computer with python 3.6.3 or greater, type `python triangles.py` to run the program on the given (default) solution.

    Optional Command Line Arguments:
    `-f filename.csv         specify input file`
    `-o filename.csv         write output to filename.csv`

    Sample output:

    With the default polygon (as seen in labeled_polygon.png)
    ```
    $ python triangles.py
    A minimum of 3 completed triangles is possible by filling any remaining points with b.
    There may be multiple valid solutions.
    ```

    On sample5.csv
    ```
    $ python triangles.py -f sample5.csv
    Fill point 13 with  a
    Fill point 12 with  a
    Fill point 14 with  a
    Fill point 20 with  a
    Fill point 18 with  a
    Fill point 15 with  b
    Fill point 19 with  b
    Fill point 21 with  b
    Fill point 16 with  b
    Fill point 17 with  b
    A minimum of 1 completed triangles is possible by filling any remaining points with b.
    There may be multiple valid solutions.

    $ python triangles.py -f sample5.csv
    Fill point 14 with  c
    Fill point 19 with  c
    Fill point 22 with  c
    Fill point 12 with  a
    Fill point 15 with  a
    Fill point 20 with  a
    Fill point 18 with  a
    A minimum of 1 completed triangles is possible by filling any remaining points with a.
    There may be multiple valid solutions.
    ```
    Output is not guaranteed to be identical across multiple runs. However, the minimum number of completed triangles will remain constant.

    Unit testing is (naively) performed by running the solution many times on each sample polygon and verifying that the output remains constant.

    To run unit tests:
    `python unitTests.py -b`

    Sample Output:
    ```
    $ python unitTests.py -b
    ........
    ----------------------------------------------------------------------
    Ran 8 tests in 0.536s

    OK
    ```

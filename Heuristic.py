from enum import Enum

# enum enumerating heuristics 

class Heuristic(Enum):
    misplaced_tiles = 0
    a_star_1 = 1
    a_star_2 = 2
    a_star_3 = 3
    iterative_deepening = 4

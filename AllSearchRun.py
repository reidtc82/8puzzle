from State import State
from Solver import solver_FIFO, solver_iterative_deepening, solver_depthFirst
from copy import deepcopy
from Heuristic import Heuristic
import time

# You can just run this file and get everything. Output isnt the best.
# So my class declarations were setting up attributes with incorrect scope. I didnt notice in development
# because I was testing one instance of the algorithm at a time
# when I uncommented all of them to let them all run one after the other the double dip implementations were
# hanging on to data from previous runs. I thought I was done with this hours ago until that popped up, now Im late to submit.
# one of those cases where Python is being as annoying as javascript
easyStart = State([[1,8,7],[3,6,0],[4,2,5]],0,[],None,0)
medStart = State([[2,0,7],[8,4,6],[1,3,5]],0,[],None,0)
hardStart = State([[5,4,3],[6,0,2],[7,8,1]],0,[],None,0)
what = State([[1,7,0],[2,8,6],[3,4,5]],0,[],None,0)
winningState = State([[1,8,7],[2,0,6],[3,4,5]],0,[],None,0)

def print_the_solution(solution):
    # This method just prints oput the path form the returned solution path object
    for sol in solution:
        solNode = sol['data']
        if 'direction' in solNode.keys():
            print('Move '+str(solNode['direction']))
        else:
            print('Starting lol First')
        print('Cost is {0}'.format(solNode['cost']))
        print('State')
        print(sol['node'].getState())

# breadth-first - dont use tile weights and no heuristic
# print('\nStarting breadth-first easy')
# d_solver = solver_FIFO(easyStart,winningState,True,None)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# print('\nStarting breadth-first med')
# d_solver = solver_FIFO(medStart,winningState,True,None)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver

# print('\nStarting breadth-first hard')
# d_solver = solver_FIFO(hardStart,winningState,True,None)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver

# # depth-first - dont use tile weights? If true it will tally but notuse them for next path to check.
# print('\nStarting depth-first easy')
# d_solver = solver_depthFirst(easyStart,winningState,True)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# print('\nStarting depth-first med')
# d_solver = solver_depthFirst(medStart,winningState,True)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# print('\nStarting depth-first hard')
# d_solver = solver_depthFirst(hardStart,winningState,True)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# # iterative deepening - dont use tile weights? If true it will tally but not use them for next path to check.
# print('\nStarting iterative-deepening easy')
# d_solver = solver_iterative_deepening(easyStart,winningState,True,Heuristic.iterative_deepening)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# print('\nStarting iterative-deepening med')
# d_solver = solver_iterative_deepening(medStart,winningState,True,Heuristic.iterative_deepening)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# print('\nStarting iterative-deepening hard')
# d_solver = solver_iterative_deepening(hardStart,winningState,True,Heuristic.iterative_deepening)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# # uniform-cost - do use tile weights and no heuristic
print('\nStarting uniform-cost easy')
d_solver = solver_FIFO(easyStart,winningState,True,Heuristic.uniform_cost)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver

print('\nStarting uniform-cost med')
d_solver = solver_FIFO(medStart,winningState,True,Heuristic.uniform_cost)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver

print('\nStarting uniform-cost hard')
d_solver = solver_FIFO(hardStart,winningState,True,Heuristic.uniform_cost)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver
#
# # best_first - do use tile weights (only just tracking them here but not counting towards solution) and uses a heuristic
# print('\nStarting best-first easy')
# d_solver = solver_FIFO(easyStart,winningState,True,Heuristic.misplaced_tiles)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# print('\nStarting best-first med')
# d_solver = solver_FIFO(medStart,winningState,True,Heuristic.misplaced_tiles)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# print('\nStarting best-first hard')
# d_solver = solver_FIFO(hardStart,winningState,True,Heuristic.misplaced_tiles)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# # A*1 - do use tile weights and uses a heuristic (per assignment - other impls. just use 1 for cost)
# print('\nStarting A*1 easy')
# d_solver = solver_FIFO(easyStart, winningState, True, Heuristic.a_star_1)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# print('\nStarting A*1 med')
# d_solver = solver_FIFO(medStart, winningState, True, Heuristic.a_star_1)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# print('\nStarting A*1 hard')
# d_solver = solver_FIFO(hardStart, winningState, True, Heuristic.a_star_1)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# # A*2 - I think this one is purely Manhattan distance and no move cost function
# print('\nStarting A*2 easy')
# d_solver = solver_FIFO(easyStart, winningState, True, Heuristic.a_star_2)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# print('\nStarting A*2 med')
# d_solver = solver_FIFO(medStart, winningState, True, Heuristic.a_star_2)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# print('\nStarting A*2 hard')
# d_solver = solver_FIFO(hardStart, winningState, True, Heuristic.a_star_2)
# d_solver.solve()
# print_the_solution(d_solver.get_path())
# print('Path steps {0}'.format(d_solver.get_steps()))
# del d_solver
#
# # A*3 - Basically manhattan distance plus cost h(n)+g(n)
# print('\nStarting A*3 easy')
# a3easy_solver = solver_FIFO(easyStart, winningState, True, Heuristic.a_star_3)
# a3easy_solver.solve()
# print_the_solution(a3easy_solver.get_path())
# print('Path steps {0}'.format(a3easy_solver.get_steps()))
# del a3easy_solver
#
# print('\nStarting A*3 med')
# a3med_solver = solver_FIFO(medStart, winningState, True, Heuristic.a_star_3)
# a3med_solver.solve()
# print_the_solution(a3med_solver.get_path())
# print('Path steps {0}'.format(a3med_solver.get_steps()))
# del a3med_solver
#
# print('\nStarting A*3 hard')
# a3hard_solver = solver_FIFO(hardStart, winningState, True, Heuristic.a_star_3)
# a3hard_solver.solve()
# print_the_solution(a3hard_solver.get_path())
# print('Path steps {0}'.format(a3hard_solver.get_steps()))
# del a3hard_solver

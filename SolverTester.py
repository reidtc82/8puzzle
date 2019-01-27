from State import State
from Solver import solver_FIFO, solver_depthFirst, solver_iterative_deepening
from copy import deepcopy
from Heuristic import Heuristic
import time

easyStart = State([[1,8,7],[3,6,0],[4,2,5]],0,[],None,0)
medStart = State([[2,0,7],[8,4,6],[1,3,5]],0,[],None,0)
hardStart = State([[5,4,3],[6,0,2],[7,8,1]],0,[],None,0)
what = State([[1,7,0],[2,8,6],[3,4,5]],0,[],None,0)
winningState = State([[1,8,7],[2,0,6],[3,4,5]],0,[],None,0)

# Set final arg to True to do Uniform-Cost

# depth-first - dont use tile weights? If true it will tally but notuse them for next path to check.
# d_solver = solver_depthFirst(easyStart,winningState,False, None)

# iterative deepening - dont use tile weights? If true it will tally but notuse them for next path to check.
d_solver = solver_iterative_deepening(easyStart,winningState,False,Heuristic.iterative_deepening)

# breadth-first - dont use tile weights and no heuristic
# d_solver = solver_FIFO(medStart,winningState,False,None)

# uniform-cost - do use tile weights and no heuristic
# d_solver = solver_FIFO(hardStart,winningState,True,None)

# best_first - do use tile weights (only just tracking them here but not counting towards solution) and uses a heuristic
# d_solver = solver_FIFO(hardStart,winningState,True,Heuristic.misplaced_tiles)

# A*1 - do use tile weights and uses a heuristic (per assignment - other impls. just use 1 for cost)
# d_solver = solver_FIFO(hardStart, winningState, True, Heuristic.a_star_1)

# A*2 - I think this one is purely Manhattan distance and no move cost function
# d_solver = solver_FIFO(medStart, winningState, True, Heuristic.a_star_2)

# A*3 - Basically manhattan distance plus cost h(n)+g(n)
# d_solver = solver_FIFO(hardStart, winningState, True, Heuristic.a_star_3)


t1 = time.time()
d_solver.solve()
t2 = time.time()
d_solution = d_solver.get_path()

for sol in d_solution:
    solNode = sol['data']
    if 'direction' in solNode.keys():
        print('Move '+str(solNode['direction']))
    else:
        print('Starting lol First')
    print('Cost is {0}'.format(solNode['cost']))
    print('State')
    print(sol['node'].getState())
print('total timed time {0}'.format(t2-t1))

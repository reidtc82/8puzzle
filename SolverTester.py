from State import State
from Solver import solver_breadthFirst, solver_depthFirst, solver_iterative_deepening
from copy import deepcopy
import time

easyStart = State([[1,8,7],[3,6,0],[4,2,5]],0,[],None,0)
medStart = State([[2,0,7],[8,4,6],[1,3,5]],0,[],None,0)
hardStart = State([[5,4,3],[6,0,2],[7,8,1]],0,[],None,0)
what = State([[1,7,0],[2,8,6],[3,4,5]],0,[],None,0)
winningState = State([[1,8,7],[2,0,6],[3,4,5]],0,[],None,0)

# Set final arg to True to do Uniform-Cost
# breadth-first
# d_solver = solver_breadthFirst(medStart,winningState,False,False)
# uniform-cost
# d_solver = solver_breadthFirst(hardStart,winningState,True,False)
# best_first
d_solver = solver_breadthFirst(hardStart,winningState,True,True)

# d_solver = solver_iterative_deepening(easyStart,winningState,False)
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

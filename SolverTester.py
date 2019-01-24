from State import State
from Solver import solver_breadthFirst, solver_depthFirst, solver_iterative_deepening
from copy import deepcopy

easyStart = State([[1,8,7],[3,6,0],[4,2,5]],0,[],None)
medStart = State([[2,0,7],[8,4,6],[1,3,5]],0,[],None)
hardStart = State([[5,4,3],[6,0,2],[7,8,1]],0,[],None)
what = State([[1,0,7],[2,8,6],[3,4,5]],0,[],None)
winningState = State([[1,8,7],[2,0,6],[3,4,5]],0,[],None)

# Set final arg to True to do Uniform-Cost
d_solver = solver_breadthFirst(hardStart,winningState,True)
d_solver.solve()
d_solution = d_solver.get_path()

# d_solver = solver_iterative_deepening(easyStart,winningState,False)
# d_solver.solve()
# d_solution = d_solver.get_path()

for sol in d_solution:
    solNode = sol['data']
    if 'direction' in solNode.keys():
        print('Move '+str(solNode['direction']))
    else:
        print('Starting Depth First')
    print('Cost is ')
    print(solNode['cost'])
    print('State')
    print(sol['node'].getState())

from State import State
from Solver import solver_breadthFirst, solver_depthFirst, solver_iterative_deepening
from copy import deepcopy

easyStart = State([[1,8,7],[3,6,0],[4,2,5]],0,[],None)
what = State([[1,0,7],[2,8,6],[3,4,5]],0,[],None)
winningState = State([[1,8,7],[2,0,6],[3,4,5]],0,[],None)

# Set final arg to True to do Uniform-Cost
# b_solver = solver_breadthFirst(easyStart,winningState,False)
# b_solver.solve()
# solution = b_solver.get_path()
#
# # test = [deepcopy(easyStart.getState()),deepcopy(winningState.getState())]
# # print(deepcopy(easyStart.getState()) not in test)
# for sol in solution:
#     solNode = sol['data']
#     if 'direction' in solNode.keys():
#         print('Move '+str(solNode['direction']))
#     else:
#         print('Starting Breadth First')
#     print('Cost is ')
#     print(solNode['cost'])
#     print('State')
#     print(sol['node'].getState())


d_solver = solver_iterative_deepening(easyStart,winningState,False)
d_solver.solve()
d_solution = d_solver.get_path()

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

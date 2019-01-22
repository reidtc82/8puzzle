from State import State
from Solver import solver_breadthFirst
from copy import deepcopy

easyStart = State([[1,8,7],[3,6,0],[4,2,5]],0,[],None)
what = State([[1,8,7],[0,2,6],[3,4,5]],0,[],None)
winningState = State([[1,8,7],[2,0,6],[3,4,5]],0,[],None)

solver = solver_breadthFirst(easyStart,winningState,False)
solver.solve()
solution = solver.get_path()

# test = [deepcopy(easyStart.getState()),deepcopy(winningState.getState())]
# print(deepcopy(easyStart.getState()) not in test)
for sol in solution:
    solNode = sol['data']
    if 'direction' in solNode.keys():
        print('Move '+str(solNode['direction']))
    else:
        print('Starting')
    print('Cost is ')
    print(solNode['cost'])
    print('State')
    print(sol['node'].getState())

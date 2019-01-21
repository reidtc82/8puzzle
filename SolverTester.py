from State import State
from Solver import solver_breadthFirst
from copy import deepcopy

easyStart = State([[1,8,7],[3,6,0],[4,2,5]],0,[])
what = State([[1,8,7],[0,2,6],[3,4,5]],0,[])
winningState = State([[1,8,7],[2,0,6],[3,4,5]],0,[])

solver = solver_breadthFirst(easyStart,winningState,False)
solution = solver.solve()

# test = [deepcopy(easyStart.getState()),deepcopy(winningState.getState())]
# print(deepcopy(easyStart.getState()) not in test)

print(solution)

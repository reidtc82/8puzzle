import numpy as np
from State import State
from copy import deepcopy

class solver_breadthFirst:
    visited = []
    queue = []
    pathTree = dict()

    def __init__(self, startingState, goalState, isUniformCost):
        self.queue.append(startingState)
        self.goalState = goalState
        self.iUC = isUniformCost
        self.pathTree[startingState] = {'parent':startingState.getParent(), 'cost':startingState.getCost()}
        self.moves = 0

    def solve(self):
        while len(self.queue) != 0:
            # print('queue length before pop')
            # print(len(self.queue))
            currentState = self.queue.pop(0)
            # print('queue length after pop')
            # print(len(self.queue))
            self.visited.append(currentState)
            # print('current')
            print(currentState.getState())
            print(self.moves)
            if np.allclose(self.goalState.getState(), currentState.getState()):
                print('***********end*************')
                return self.returnPath(self.pathTree[currentState], [])
                break
            else:
                for child in self.successors(currentState):
                    # print('visited')
                    # print(self.visited)
                    if not self.check_visited(child):
                        # print('queue')
                        # print(self.queue)
                        if not self.check_queue(child):
                            #store info from when created in successor funciton.
                            # print('child')
                            # print(child.getState())
                            self.pathTree[child] = {'parent':child.getParent(), 'cost':child.getCost()}
                            #append because breadth first. Use insert for depth first.
                            self.queue.append(child)
                    #ha I think one tab was messing me up
                    self.visited.append(currentState)
            self.moves += 1
            if len(self.queue) > 1000:
                break

    def check_visited(self, child):
        result = False
        for v in self.visited:
            if np.allclose(v.getState(), child.getState()):
                result = True
                break
        return result

    def check_queue(self, child):
        result = False
        for q in self.queue:
            if np.allclose(q.getState(), child.getState()):
                result = True
                break
        return result

    def successors(self, root):
        successors = []
        zero_x = root.getZeroLocation()['col']
        zero_y = root.getZeroLocation()['row']
        temp = root.getState()#wtf python?! I couldnt just pass root.getState() to deepcopy, no, that didnt make a copy. I had to do it like this...

        # dont forget to go back and deal with all these ridiculous variables
        newLState = deepcopy(temp)
        newRState = deepcopy(temp)
        newUState = deepcopy(temp)
        newDState = deepcopy(temp)
        #inverted y axis

        if zero_x != 0:
            #take left child
            leftTile = newLState[zero_x-1][zero_y]
            newLState[zero_x-1][zero_y] = 0
            newLState[zero_x][zero_y] = leftTile

            cost = leftTile if self.iUC else 1
            leftNew = State(newLState,cost,root)

            successors.append(leftNew)

        if zero_x != 2:
            #take right child
            rightTile = newRState[zero_x+1][zero_y]
            newRState[zero_x+1][zero_y] = 0
            newRState[zero_x][zero_y] = rightTile

            cost = rightTile if self.iUC else 1
            rightNew = State(newRState,cost,root)

            successors.append(rightNew)

        if zero_y != 0:
            #take upper child
            upTile = newUState[zero_x][zero_y-1]
            newUState[zero_x][zero_y-1] = 0
            newUState[zero_x][zero_y] = upTile

            cost = upTile if self.iUC else 1
            upNew = State(newUState,cost,root)

            successors.append(upNew)

        if zero_y != 2:
            #take lower child
            downTile = newDState[zero_x][zero_y+1]
            newDState[zero_x][zero_y+1] = 0
            newDState[zero_x][zero_y] = downTile

            cost = downTile if self.iUC else 1
            downNew = State(newDState,cost,root)

            successors.append(downNew)

        return successors

    def returnPath(self, node, path):
        #returns list of dicts to use to define solution. Evrything should be in visited
        if self.pathTree[node][parent] == None:
            path.append(node)
            return path
        else:
            path.append(node)
            self.returnPath(self.pathTree[node][parent], path)

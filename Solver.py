import numpy as np
from State import State
from copy import deepcopy
from Direction import Direction
import time
import math

class solver_iterative_deepening:
    visited = set()
    queue = []
    queue_track = set()
    pathTree = dict()
    path = []

    def __init__(self, startingState, goalState, isUniformCost):
        self.queue.append(startingState)
        self.queue_track.add(repr(startingState.getState()))
        self.goalState = goalState
        self.iUC = isUniformCost
        self.pathTree[startingState] = {'parent':startingState.getParent(), 'cost':startingState.getCost()}
        self.moves = 0
        self.start_state = startingState

    def solve(self):
        t0 = time.time()
        current_depth = 0

        for i in range(0, 5):
            while not self.is_empty(self.queue):
                # print('at depth {0}'.format(current_depth))
                # print('queue length before pop')
                # print(len(self.queue))
                currentState = self.queue.pop(0)
                self.queue_track.remove(repr(currentState.getState()))
                current_depth = currentState.getDepth()
                # print(currentState.getState())
                # print('queue length after pop')
                # print(len(self.queue))
                self.visited.add(repr(currentState.getState()))

                if self.moves%1 == 0:
                    print("Yes I'm still working current moves: {0} ".format(self.moves)+" current queue length: {0}".format(len(self.queue))+" current depth: {0}".format(current_depth))

                if np.allclose(self.goalState.getState(), currentState.getState()):
                    print('***********end*************')
                    self.returnPath(currentState)
                    break
                elif current_depth <= i:
                    for child in self.successors(currentState):
                        # print('visited')
                        # print(self.visited)
                        # print(self.check_visited(child))
                        if not self.check_visited(child):
                            # print('queue')
                            # print(self.queue)
                            if not self.check_queue(child):
                                #store info from when created in successor funciton.
                                # print('child')
                                # print(child.getState())
                                self.pathTree[child] = {'parent':child.getParent(), 'cost':child.getCost(), 'direction':child.getDirection()}
                                #append because breadth first. Use insert for depth first.
                                self.queue.insert(0, child)
                                self.queue_track.add(repr(child.getState()))
                        #ha I think one tab was messing me up
                        # self.visited[currentState.getState()] = True

                self.moves += 1
                if self.moves > 10:
                    t1 = time.time()
                    print(t1-t0)
                    break

            #start over
            self.queue.append(self.start_state)
            self.queue_track.add(repr(self.start_state.getState()))
            # self.goalState = goalState
            # self.iUC = isUniformCost
            self.pathTree[self.start_state] = {'parent':self.start_state.getParent(), 'cost':self.start_state.getCost()}
            # self.moves = 0
            current_depth = 0
            self.visited.clear()

    def check_visited(self, child):
        result = False
        # for v in self.visited:
        #     if np.allclose(v.getState(), child.getState()):
        #         result = True
        #         break
        if repr(child.getState()) in self.visited:
            result = True
        # try:
        #     if self.visited[child.getState()]:
        #         result = True
        # except:
        #     pass
        return result

    def check_queue(self, child):
        result = False
        # for q in self.queue:
        #     if np.allclose(q.getState(), child.getState()):
        #         result = True
        #         break
        if repr(child.getState()) in self.queue_track:
            result = True
        return result

    def successors(self, root):
        successors = []
        zero_x = root.getZeroLocation()['col']
        zero_y = root.getZeroLocation()['row']
        temp = root.getState()#wtf python?! I couldnt just pass root.getState() to deepcopy, no, that didnt make a copy. I had to do it like this...
        depth = root.getDepth()+1
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
            leftNew = State(newLState,cost,root,Direction.LEFT,depth)

            successors.insert(0,leftNew)

        if zero_x != 2:
            #take right child
            rightTile = newRState[zero_x+1][zero_y]
            newRState[zero_x+1][zero_y] = 0
            newRState[zero_x][zero_y] = rightTile

            cost = rightTile if self.iUC else 1

            rightNew = State(newRState,cost,root,Direction.RIGHT,depth)

            successors.insert(0,rightNew)

        if zero_y != 0:
            #take upper child
            upTile = newUState[zero_x][zero_y-1]
            newUState[zero_x][zero_y-1] = 0
            newUState[zero_x][zero_y] = upTile

            cost = upTile if self.iUC else 1
            upNew = State(newUState,cost,root,Direction.UP,depth)

            successors.insert(0,upNew)

        if zero_y != 2:
            #take lower child
            downTile = newDState[zero_x][zero_y+1]
            newDState[zero_x][zero_y+1] = 0
            newDState[zero_x][zero_y] = downTile

            cost = downTile if self.iUC else 1
            downNew = State(newDState,cost,root,Direction.DOWN,depth)

            successors.insert(0,downNew)

        return successors

    def returnPath(self, node):
        #returns list of dicts to use to define solution. Evrything should be in visited
        # for n in self.pathTree:
        #     print(self.pathTree[n])
        # print(self.pathTree[node]['parent'])
        while self.pathTree[node]['parent'] != []:
            self.path.insert(0, {'node':node, 'data':self.pathTree[node]})
            node = self.pathTree[node]['parent']

    def get_path(self):
        return self.path

    def is_empty(self,ls):
        return False if ls else True

#----------------------------------------------------

class solver_depthFirst:
    visited = set()
    queue = []
    queue_track = set()
    pathTree = dict()
    path = []

    def __init__(self, startingState, goalState, isUniformCost):
        self.queue.append(startingState)
        self.queue_track.add(repr(startingState.getState()))
        self.goalState = goalState
        self.iUC = isUniformCost
        self.pathTree[startingState] = {'parent':startingState.getParent(), 'cost':startingState.getCost()}
        self.moves = 0

    def solve(self):
        t0 = time.time()
        while not self.is_empty(self.queue):
            if self.moves%10000 == 0:
                print("Yes I'm still working current moves: {0} ".format(self.moves)+" current queue length: {0}".format(len(self.queue)))
            # print('queue length before pop')
            # print(len(self.queue))
            currentState = self.queue.pop(0)
            self.queue_track.remove(repr(currentState.getState()))
            # print(currentState.getState())
            # print('queue length after pop')
            # print(len(self.queue))
            self.visited.add(repr(currentState.getState()))
            if np.allclose(self.goalState.getState(), currentState.getState()):
                print('***********end*************')
                self.returnPath(currentState)
                break
            else:
                for child in self.successors(currentState):
                    # print('visited')
                    # print(self.visited)
                    # print(self.check_visited(child))
                    if not self.check_visited(child):
                        # print('queue')
                        # print(self.queue)
                        if not self.check_queue(child):
                            #store info from when created in successor funciton.
                            # print('child')
                            # print(child.getState())
                            self.pathTree[child] = {'parent':child.getParent(), 'cost':child.getCost(), 'direction':child.getDirection()}
                            #append because breadth first. Use insert for depth first.
                            self.queue.insert(0, child)
                            self.queue_track.add(repr(child.getState()))
                    #ha I think one tab was messing me up
                    # self.visited[currentState.getState()] = True
            self.moves += 1
            if self.moves > 1000000:
                t1 = time.time()
                print(t1-t0)
                break

    def check_visited(self, child):
        result = False
        # for v in self.visited:
        #     if np.allclose(v.getState(), child.getState()):
        #         result = True
        #         break
        # speed bump - apply this to BFS?
        if repr(child.getState()) in self.visited:
            result = True
        # try:
        #     if self.visited[child.getState()]:
        #         result = True
        # except:
        #     pass
        return result

    def check_queue(self, child):
        result = False
        # for q in self.queue:
        #     if np.allclose(q.getState(), child.getState()):
        #         result = True
        #         break
        # speed bump - apply this to BFS?
        if repr(child.getState()) in self.queue_track:
            result = True
        return result

    def successors(self, root):
        successors = []
        zero_x = root.getZeroLocation()['col']
        zero_y = root.getZeroLocation()['row']
        temp = root.getState()#wtf python?! I couldnt just pass root.getState() to deepcopy, no, that didnt make a copy. I had to do it like this...
        depth = 1
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
            leftNew = State(newLState,cost,root,Direction.LEFT,depth)

            successors.insert(0,leftNew)

        if zero_x != 2:
            #take right child
            rightTile = newRState[zero_x+1][zero_y]
            newRState[zero_x+1][zero_y] = 0
            newRState[zero_x][zero_y] = rightTile

            cost = rightTile if self.iUC else 1
            rightNew = State(newRState,cost,root,Direction.RIGHT,depth)

            successors.insert(0,rightNew)

        if zero_y != 0:
            #take upper child
            upTile = newUState[zero_x][zero_y-1]
            newUState[zero_x][zero_y-1] = 0
            newUState[zero_x][zero_y] = upTile

            cost = upTile if self.iUC else 1
            upNew = State(newUState,cost,root,Direction.UP,depth)

            successors.insert(0,upNew)

        if zero_y != 2:
            #take lower child
            downTile = newDState[zero_x][zero_y+1]
            newDState[zero_x][zero_y+1] = 0
            newDState[zero_x][zero_y] = downTile

            cost = downTile if self.iUC else 1
            downNew = State(newDState,cost,root,Direction.DOWN,depth)

            successors.insert(0,downNew)

        return successors

    def returnPath(self, node):
        #returns list of dicts to use to define solution. Evrything should be in visited
        # for n in self.pathTree:
        #     print(self.pathTree[n])
        # print(self.pathTree[node]['parent'])
        while self.pathTree[node]['parent'] != []:
            self.path.insert(0, {'node':node, 'data':self.pathTree[node]})
            node = self.pathTree[node]['parent']

    def get_path(self):
        return self.path

    def is_empty(self,ls):
        return False if ls else True

#----------------------------------------------------

class solver_breadthFirst:
    visited = []
    queue = []
    pathTree = dict()
    path = []

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
            if np.allclose(self.goalState.getState(), currentState.getState()):
                print('***********end*************')
                self.returnPath(currentState)
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
                            # print(temp.getCost())
                            self.pathTree[child] = {'parent':child.getParent(), 'cost':child.getCost(), 'direction':child.getDirection()}
                            # append because breadth first. Use insert for depth first.
                            self.queue.append(child)
                        else:
                            #I'm not 100% sure this is working... It never finds a cheaper node so it never swaps.
                            # so many loops, so slow... But the professor said its OK to over-engineer just to get it to work.
                            # print('found one preexisting')
                            for q in self.queue:
                                if np.allclose(q.getState(), child.getState()):
                                    # print(q.getDirection())
                                    # print(child.getDirection())
                                    if child.getCost() < q.getCost():
                                        print('found a cheaper one')
                                        q.setCost(child.getCost())
                                        q.setParent(child.getParent())
                                        q.setDirection(child.getDirection())
                                        self.pathTree[q] = {'parent':q.getParent(), 'cost':q.getCost(), 'direction':q.getDirection()}

                            # accomodate cost and overwrite if less with new cost and parent
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
        depth = 1
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

            cost = leftTile+root.getCost() if self.iUC else 1+root.getCost()
            leftNew = State(newLState,cost,root,Direction.LEFT,depth)

            successors.append(leftNew)

        if zero_x != 2:
            #take right child
            rightTile = newRState[zero_x+1][zero_y]
            newRState[zero_x+1][zero_y] = 0
            newRState[zero_x][zero_y] = rightTile

            cost = rightTile+root.getCost() if self.iUC else 1+root.getCost()
            rightNew = State(newRState,cost,root,Direction.RIGHT,depth)

            successors.append(rightNew)

        if zero_y != 0:
            #take upper child
            upTile = newUState[zero_x][zero_y-1]
            newUState[zero_x][zero_y-1] = 0
            newUState[zero_x][zero_y] = upTile

            cost = upTile+root.getCost() if self.iUC else 1+root.getCost()
            upNew = State(newUState,cost,root,Direction.UP,depth)

            successors.append(upNew)

        if zero_y != 2:
            #take lower child
            downTile = newDState[zero_x][zero_y+1]
            newDState[zero_x][zero_y+1] = 0
            newDState[zero_x][zero_y] = downTile

            cost = downTile+root.getCost() if self.iUC else 1+root.getCost()
            downNew = State(newDState,cost,root,Direction.DOWN,depth)

            successors.append(downNew)

        return successors

    def returnPath(self, node):
        #returns list of dicts to use to define solution. Evrything should be in visited
        # for n in self.pathTree:
        #     print(self.pathTree[n])
        # print(self.pathTree[node]['parent'])
        self.path.insert(0, {'node':node, 'data':self.pathTree[node]})
        if self.pathTree[node]['parent'] != []:
            self.returnPath(self.pathTree[node]['parent'])

    def get_path(self):
        return self.path

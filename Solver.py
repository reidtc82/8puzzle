import numpy as np
from State import State
from copy import deepcopy
from Direction import Direction
from Heuristic import Heuristic
import time
import math

# Im a bit all over the place when it comes to style and OOP-ness.

class solver_iterative_deepening:
    # Just the class
    visited = set()
    queue = []
    queue_track = set()
    pathTree = dict()
    path = []
    steps = 0

    def __init__(self, startingState, goalState, useTileWeights, heuristic):
        # Constructor - I tried using this class for both iterative-deepening and
        # depth-first as I did with the BFS variants but it wasnt having it. the
        # heuristic attribute is meaningless.
        self.queue.append(startingState)
        self.queue_track.add(repr(startingState.getState()))
        self.goalState = goalState
        self.useTileWeights = useTileWeights
        self.pathTree[startingState] = {'parent':startingState.getParent(), 'cost':startingState.getCost()}
        self.moves = 0
        self.start_state = startingState
        self.win = False
        self.maxQueueLen = 0
        self.maxVisited = 0
        self.heuristic = heuristic


    def solve(self):
        # This is the actual search. Instantiate the class then run solveself.
        # See the SolverTester.py file.
        t0 = time.time()
        current_depth = 0

        # Artifacts from trying to double dip with this class. Below would
        # crash the thing, but baking in the ranges is fine??
        # if self.heuristic == Heuristic.iterative_deepening:
        #     self.rangeStart = range(math.factorial(9))
        # else:
        #     self.rangeStart = range(math.factorial(9)-1,math.factorial(9))

        # So, baked in ranges are fine with my code but trying to change them didnt work...
        # Basically this can be converted to DFS by setting the range to
        # range(math.factorial(9)-1, math.factorial(9))
        # Im not experienced enough nor do I have the time to figure it out so DFS is at the bottom
        for i in range(math.factorial(9)):
            # Inside the level/depth loop
            # Just an auto kill switch
            if time.time() - t0 > 300:
                print('Queue length so far {0}'.format(self.maxQueueLen))
                print('visited count so far {0}'.format(self.maxVisited))
                print('Iterative deepening exceeded 5 minutes. Stopping')
                break

            while not self.is_empty(self.queue):
                # Familiar main loop with a kill switch
                if time.time() - t0 > 300:
                    print('Queue length so far {0}'.format(self.maxQueueLen))
                    print('visited count so far {0}'.format(self.maxVisited))
                    print('Iterative deepening exceeded 5 minutes. Stopping')
                    break

                # Tracking max queue length for memory use reporting
                if len(self.queue) > self.maxQueueLen:
                    self.maxQueueLen = len(self.queue)

                # popping the first queued state
                currentState = self.queue.pop(0)
                # So... this is the result of my poor skillset
                # Basically this algorithm was taking way too long
                # This second queue is indexed by the string of the State
                # because Python wont let me index by the object state
                # It allows me to check queued faster and still maintain all the data
                self.queue_track.remove(repr(currentState.getState()))
                current_depth = currentState.getDepth()

                # visited didnt need to data so just storing the str representation of the state
                self.visited.add(repr(currentState.getState()))
                # and tracking max visited
                if self.maxVisited < len(self.visited):
                    self.maxVisited = len(self.visited)

                # sanity check
                if self.moves%1000 == 0:
                    print("Yes I'm still working current queue length: {0}".format(len(self.queue)))

                # did we win?
                if np.allclose(self.goalState.getState(), currentState.getState()):
                    print('***********end*************')
                    print('Queue length {0}'.format(self.maxQueueLen))
                    print('visited count {0}'.format(self.maxVisited))
                    self.win = True
                    self.returnPath(currentState)
                    break
                elif current_depth < i:
                # Nope, didnt win
                    for child in self.successors(currentState):
                        if not self.check_visited(child):
                            if not self.check_queue(child):
                                #store info from when created in successor funciton.
                                self.pathTree[child] = {'parent':child.getParent(), 'cost':child.getCost(), 'direction':child.getDirection()}
                                #append because breadth first. Use insert for depth first.
                                self.queue.insert(0, child)
                                self.queue_track.add(repr(child.getState()))

                self.moves += 1

            if not self.win:
                self.start_again()
            else:
                break

    def start_again(self):
        if not self.win:
            #start over
            self.reset_start_state()
            self.queue.append(self.start_state)
            self.queue_track.add(repr(self.start_state.getState()))
            self.pathTree[self.start_state] = {'parent':self.start_state.getParent(), 'cost':self.start_state.getCost()}
            current_depth = 0
            self.visited.clear()

    def reset_start_state(self):
        self.start_state.setCost(0)
        self.start_state.setDirection(None)
        self.start_state.setParent(None)
        self.start_state.set_depth(0)

    def check_visited(self, child):
        result = False

        if repr(child.getState()) in self.visited:
            result = True

        return result

    def check_queue(self, child):
        result = False

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

            cost = leftTile+root.getCost() if self.useTileWeights else 1+root.getCost()
            leftNew = State(newLState,cost,root,Direction.LEFT,depth)

            successors.insert(0,leftNew)

        if zero_x != 2:
            #take right child
            rightTile = newRState[zero_x+1][zero_y]
            newRState[zero_x+1][zero_y] = 0
            newRState[zero_x][zero_y] = rightTile

            cost = rightTile+root.getCost() if self.useTileWeights else 1+root.getCost()

            rightNew = State(newRState,cost,root,Direction.RIGHT,depth)

            successors.insert(0,rightNew)

        if zero_y != 0:
            #take upper child
            upTile = newUState[zero_x][zero_y-1]
            newUState[zero_x][zero_y-1] = 0
            newUState[zero_x][zero_y] = upTile

            cost = upTile+root.getCost() if self.useTileWeights else 1+root.getCost()
            upNew = State(newUState,cost,root,Direction.UP,depth)

            successors.insert(0,upNew)

        if zero_y != 2:
            #take lower child
            downTile = newDState[zero_x][zero_y+1]
            newDState[zero_x][zero_y+1] = 0
            newDState[zero_x][zero_y] = downTile

            cost = downTile+root.getCost() if self.useTileWeights else 1+root.getCost()
            downNew = State(newDState,cost,root,Direction.DOWN,depth)

            successors.insert(0,downNew)

        return successors

    def returnPath(self, node):
        # creates list of dicts to use to define solution. Evrything should be in visited
        steps = 0
        while self.pathTree[node]['parent']:
            steps += 1
            self.path.insert(0, {'node':node, 'data':self.pathTree[node]})
            node = self.pathTree[node]['parent']

        self.set_steps(steps)

    def get_path(self):
        return self.path

    def is_empty(self,ls):
        return False if ls else True

    def set_steps(self, steps):
        self.steps = steps

    def get_steps(self):
        return self.steps

#----------------------------------------------------
class solver_FIFO:
    visited = []
    queue = []
    pathTree = dict()
    path = []
    steps = 0

    def __init__(self, startingState, goalState, useTileWeights, heuristic):
        self.queue.append(startingState)
        self.goalState = goalState
        self.useTileWeights = useTileWeights
        self.pathTree[startingState] = {'parent':startingState.getParent(), 'cost':startingState.getCost()}
        self.moves = 0
        self.heuristic = heuristic
        self.maxQueueLen = 0

    def solve(self):
        t0 = time.time()
        while len(self.queue) != 0:
            if time.time() - t0 > 300:
                print('Queue length {0}'.format(self.maxQueueLen))
                print('visited count {0}'.format(len(self.visited)))
                print('FIFO - Whichever one this is - exceeded 5 minutes. Stopping')
                break

            if self.moves%100 == 0:
                print('Yes Im still working: {0}'.format(self.moves))

            if len(self.queue) > self.maxQueueLen:
                self.maxQueueLen = len(self.queue)

            currentState = self.queue.pop(self.find_lowest_cost_index())

            self.visited.append(currentState)

            if np.allclose(self.goalState.getState(), currentState.getState()):
                print('***********end*************')
                print('visited count {0}'.format(len(self.visited)))
                print('max queue length {0}'.format(self.maxQueueLen))
                self.returnPath(currentState)
                break
            else:
                for child in self.successors(currentState):
                    if not self.check_visited(child):
                        #store info from when created in successor funciton.
                        if not self.check_queue(child):
                            if not self.heuristic:
                                self.pathTree[child] = {'parent':child.getParent(), 'cost':child.getCost(), 'direction':child.getDirection()}
                            else:
                                self.pathTree[child] = {'parent':child.getParent(), 'cost':child.getCost(), 'direction':child.getDirection(), 'heuristic':child.get_h_cost()}
                            # append because breadth first. Use insert for depth first.
                            self.queue.append(child)
                        else:
                            for q in self.queue:
                                if np.allclose(q.getState(), child.getState()):
                                    if self.heuristic == None:
                                        if child.getCost() < q.getCost(): #if its <= then breadth first will mess up
                                            q.setCost(child.getCost())
                                            q.setParent(child.getParent())
                                            q.setDirection(child.getDirection())
                                            self.pathTree[q] = {'parent':q.getParent(), 'cost':q.getCost(), 'direction':q.getDirection()}

                                    else:
                                        if child.get_h_cost() < q.get_h_cost():
                                            q.setCost(child.getCost())
                                            q.setParent(child.getParent())
                                            q.setDirection(child.getDirection())
                                            q.set_h_cost(child.get_h_cost())
                                            self.pathTree[q] = {'parent':q.getParent(), 'cost':q.getCost(), 'direction':q.getDirection(), 'heuristic':q.get_h_cost()}

                    self.visited.append(currentState)

            self.moves += 1

    def _heuristic(self, h, state):
        s1 = state.getState()
        s2 = self.goalState.getState()
        result = 0
        # seems like I shouldnt could 0 position
        if h == Heuristic.misplaced_tiles or h == Heuristic.a_star_1:
            for i in range(3):
                for j in range(3):
                    if s1[i][j] != s2[i][j]:
                        result += 1
            if h == Heuristic.a_star_1:
                # this should be sum of move costs = 1 if A*1 was called with correct args
                result += state.getCost()

        elif h == Heuristic.a_star_2:
            # Manhattan distance alone?
            result += self.sum_of_manhattan_distance(s1, s2)

        elif h == Heuristic.a_star_3:
            # I feel like this is cheating but it works.
            result += self.sum_of_manhattan_distance(s1, s2)+state.getCost()

        return result

    def sum_of_manhattan_distance(self, s1, s2):
        mD = [0] *9
        result = 0
        for i in range(3):
            for j in range(3):
                # get the position of the goal values indexed by the value
                mD[s2[i][j]] = [i,j]
        for i in range(3):
            for j in range(3):
                # sum of Manhattan distances of each value in the current state
                # basically, find the index of the current value in mD and get its position in the goal state
                # subtract the current position from that
                # add the absolute values of those differences together for Manhattan distance of these values
                # add to the total
                # confusing enough?
                # sum(abs(goal(x)-current(x)), abs(goal(y)-current(y))) for whatever value we're on currently
                result += abs(mD[s1[i][j]][0] - i)+abs(mD[s1[i][j]][1] - j)
        return result

    def find_lowest_cost_index(self):
        lowest = 0
        for i in range(len(self.queue)):
            # print(self.heuristic(self.queue[i].getState()))
            if self.heuristic:
                if self.queue[i].get_h_cost() < self.queue[lowest].get_h_cost():
                    lowest = i
            else:
                if self.queue[i].getCost() < self.queue[lowest].getCost():
                    # print('Im the cheapest {0}'.format(i)+' of queue length {0}'.format(len(self.queue)))
                    lowest = i
        return lowest

    def check_visited(self, child):
        result = False
        for v in self.visited:
            if np.allclose(v.getState(), child.getState()):
                result = True
                break
        return result

    def check_queue(self, child):
        result = False
        for cq in self.queue:
            if np.allclose(cq.getState(), child.getState()):
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

            cost = leftTile+root.getCost() if self.useTileWeights else 1+root.getCost()
            leftNew = State(newLState,cost,root,Direction.LEFT,depth)
            leftNew.set_h_cost(self._heuristic(self.heuristic, leftNew))

            successors.append(leftNew)
            del leftNew

        if zero_x != 2:
            #take right child
            rightTile = newRState[zero_x+1][zero_y]
            newRState[zero_x+1][zero_y] = 0
            newRState[zero_x][zero_y] = rightTile

            cost = rightTile+root.getCost() if self.useTileWeights else 1+root.getCost()
            rightNew = State(newRState,cost,root,Direction.RIGHT,depth)
            rightNew.set_h_cost(self._heuristic(self.heuristic, rightNew))

            successors.append(rightNew)
            del rightNew

        if zero_y != 0:
            #take upper child
            upTile = newUState[zero_x][zero_y-1]
            newUState[zero_x][zero_y-1] = 0
            newUState[zero_x][zero_y] = upTile

            cost = upTile+root.getCost() if self.useTileWeights else 1+root.getCost()
            upNew = State(newUState,cost,root,Direction.UP,depth)
            upNew.set_h_cost(self._heuristic(self.heuristic, upNew))

            successors.append(upNew)
            del upNew

        if zero_y != 2:
            #take lower child
            downTile = newDState[zero_x][zero_y+1]
            newDState[zero_x][zero_y+1] = 0
            newDState[zero_x][zero_y] = downTile

            cost = downTile+root.getCost() if self.useTileWeights else 1+root.getCost()
            downNew = State(newDState,cost,root,Direction.DOWN,depth)
            downNew.set_h_cost(self._heuristic(self.heuristic, downNew))

            successors.append(downNew)
            del downNew

        return successors

    def returnPath(self, node):
        # creates list of dicts to use to define solution. Evrything should be in visited
        steps = 0
        while self.pathTree[node]['parent']:
            steps += 1
            self.path.insert(0, {'node':node, 'data':self.pathTree[node]})
            node = self.pathTree[node]['parent']

        self.set_steps(steps)

    def get_path(self):
        return self.path

    def set_steps(self, steps):
        self.steps = steps

    def get_steps(self):
        return self.steps


#----------------------------------------------------
class solver_depthFirst:
    visited = set()
    queue = []
    queue_track = set()
    pathTree = dict()
    path = []
    steps = 0

    def __init__(self, startingState, goalState, useTileWeights):
        self.queue.append(startingState)
        self.queue_track.add(repr(startingState.getState()))
        self.goalState = goalState
        self.useTileWeights = useTileWeights
        self.pathTree[startingState] = {'parent':startingState.getParent(), 'cost':startingState.getCost()}
        self.moves = 0
        self.maxQueueLen = 0

    def solve(self):
        t0 = time.time()
        while not self.is_empty(self.queue):
            if time.time() - t0 > 300:
                print('Queue length {0}'.format(self.maxQueueLen))
                print('visited count {0}'.format(len(self.visited)))
                print('DFS exceeded 5 minutes. Stopping')
                break

            if self.moves%1000 == 0:
                print("Yes I'm still working current queue length: {0}".format(len(self.queue)))

            if len(self.queue) > self.maxQueueLen:
                self.maxQueueLen = len(self.queue)
            currentState = self.queue.pop(0)
            self.queue_track.remove(repr(currentState.getState()))

            self.visited.add(repr(currentState.getState()))
            if np.allclose(self.goalState.getState(), currentState.getState()):
                print('***********end*************')
                print('Queue length {0}'.format(self.maxQueueLen))
                print('visited count {0}'.format(len(self.visited)))
                self.returnPath(currentState)
                break
            else:
                for child in self.successors(currentState):
                    if not self.check_visited(child):
                        if not self.check_queue(child):
                            #store info from when created in successor funciton.
                            self.pathTree[child] = {'parent':child.getParent(), 'cost':child.getCost(), 'direction':child.getDirection()}
                            #append because breadth first. Use insert for depth first.
                            self.queue.insert(0, child)
                            self.queue_track.add(repr(child.getState()))

            self.moves += 1


    def check_visited(self, child):
        result = False

        if repr(child.getState()) in self.visited:
            result = True

        return result

    def check_queue(self, child):
        result = False

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

            cost = leftTile+root.getCost() if self.useTileWeights else 1+root.getCost()
            leftNew = State(newLState,cost,root,Direction.LEFT,depth)

            successors.insert(0,leftNew)

        if zero_x != 2:
            #take right child
            rightTile = newRState[zero_x+1][zero_y]
            newRState[zero_x+1][zero_y] = 0
            newRState[zero_x][zero_y] = rightTile

            cost = rightTile+root.getCost() if self.useTileWeights else 1+root.getCost()
            rightNew = State(newRState,cost,root,Direction.RIGHT,depth)

            successors.insert(0,rightNew)

        if zero_y != 0:
            #take upper child
            upTile = newUState[zero_x][zero_y-1]
            newUState[zero_x][zero_y-1] = 0
            newUState[zero_x][zero_y] = upTile

            cost = upTile+root.getCost() if self.useTileWeights else 1+root.getCost()
            upNew = State(newUState,cost,root,Direction.UP,depth)

            successors.insert(0,upNew)

        if zero_y != 2:
            #take lower child
            downTile = newDState[zero_x][zero_y+1]
            newDState[zero_x][zero_y+1] = 0
            newDState[zero_x][zero_y] = downTile

            cost = downTile+root.getCost() if self.useTileWeights else 1+root.getCost()
            downNew = State(newDState,cost,root,Direction.DOWN,depth)

            successors.insert(0,downNew)

        return successors

    def returnPath(self, node):
        # creates list of dicts to use to define solution. Evrything should be in visited
        steps = 0
        while self.pathTree[node]['parent']:
            steps += 1
            self.path.insert(0, {'node':node, 'data':self.pathTree[node]})
            node = self.pathTree[node]['parent']

        self.set_steps(steps)

    def get_path(self):
        return self.path

    def is_empty(self,ls):
        return False if ls else True

    def set_steps(self, steps):
        self.steps = steps

    def get_steps(self):
        return self.steps

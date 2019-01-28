# Reid Case
# Assignment 1
#
# This file is everything all in one. Just run it.
#

from enum import Enum
import numpy as np
from copy import deepcopy
import time
import math

# enum enumerating directions
class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

# enumerating heuristics
class Heuristic(Enum):
    misplaced_tiles = 0
    a_star_1 = 1
    a_star_2 = 2
    a_star_3 = 3
    iterative_deepening = 4
    uniform_cost = 5

################################################################################################################################
# State class
class State:
    def __init__(self, state, cost, parent, dir, dep):
        # constructor
        # letting the state object store all of its info. Probably not the best approach in hindsight
        self.state = state
        self.cost = cost
        self.parent = parent
        self.queued = False
        self.visited = False
        self.direction = dir
        self.depth = dep
        self.hCost = 0
    # def __eq__(self, notSelf):
    #     return self.state == notSelf.getState() and self.cost == notSelf.getCost() and self.parent == notSelf.getParent()

    # standard accessors
    def getState(self):
        # returns list of the actual tile value arrangement
        return self.state

    def getCost(self):
        # returns the cost g(n)
        return self.cost

    def getParent(self):
        # returns parent state
        return self.parent

    def setCost(self, pathCost):
        # allows changing of the cost
        self.cost = pathCost

    def setParent(self, parent):
        # allows changing of the parent
        self.parent = parent

    # for the GUI that never came to be
    def getZeroLocation(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    zero_location = {'col':i,'row':j}
        return zero_location

    def getDirection(self):
        # direction moved to get to this state
        return self.direction

    def setDirection(self, dir):
        # sets the direction
        self.direction = dir

    def getDepth(self):
        # not really used now that I think about it
        # returns depth
        return self.depth

    def set_depth(self, dep):
        # sets depth
        # intended for IDS but never used
        self.depth = dep

    def set_h_cost(self, hCost):
        # sets h(n)
        self.hCost = hCost

    def get_h_cost(self):
        # returns h(n)
        return self.hCost


################################################################################################################################
# Solvers
# Im a bit all over the place when it comes to style and OOP-ness.
# Sorry for not refactoring all the shared code between classes into a utility package

# Multi-dipped for this one
# These are all memory intensive really
# They are all greedy, taking the lowest cost or heuristic cost for the next node to explore
class solver_FIFO:
    def __init__(self, startingState, goalState, useTileWeights, heuristic):
        # Constructor - useTileWeights and heuristic to determine which search
        # strategy to use - See Heuristic enum for options here
        # Wonderfull, nearly 12 hours and counting wasted because of class scope issues... now its a late submission and I dont get to sleep tonight
        self.visited = set()
        self.queue = []
        self.pathTree = dict()
        self.queue_track = set()
        self.path = []
        self.steps = 0
        self.mD = [0] *9
        self.queue.append(startingState)
        self.queue_track.add(repr(startingState.getState()))
        self.goalState = goalState
        self.useTileWeights = useTileWeights
        self.pathTree[startingState] = {'parent':startingState.getParent(), 'cost':startingState.getCost()}
        self.moves = 0
        self.heuristic = heuristic
        self.maxQueueLen = 0
        for i in range(3):
            for j in range(3):
                # get the position of the goal values indexed by the value
                self.mD[goalState.getState()[i][j]] = [i,j]
        print(len(self.queue))

    def solve(self):
        # solver for FIFOs
        t0 = time.time()
        while len(self.queue) != 0:
            # Inside main loop for BFS and variants
            if time.time() - t0 > 300:
                # kill switch
                print('Queue length {0}'.format(self.maxQueueLen))
                print('visited count {0}'.format(len(self.visited)))
                print('FIFO - Whichever one this is - exceeded 5 minutes. Stopping')
                self.visited = set()
                self.queue = []
                self.pathTree = dict()
                self.queue_track = set()
                self.path = []
                self.steps = 0
                self.mD = [0] *9
                break

            # sanity checking
            self.moves += 1
            if self.moves%10000 == 0:
                print('Yes Im still working: {0}'.format(len(self.queue)))

            # tracking for reporting
            if len(self.queue) > self.maxQueueLen:
                self.maxQueueLen = len(self.queue)

            # Popping the node with the index that is returned
            # I could sort but if I jsut give it the lowest its a little faster I think
            # Sorting would take more operations, finding the lowest takes a single pass through the queue
            if self.heuristic:
                currentState = self.queue.pop(self.find_lowest_cost_index())
            else:
                # if I dont pass a heuristic this is just BFS
                currentState = self.queue.pop(0)

            # used to keep track of queue.
            # lists are ordered, sets and dict are notself.# dict I can index iwth the state object
            # set I can find membership quickly but cant index with the state object so I stringify the state
            self.queue_track.remove(repr(currentState.getState()))

            # seems early but we have popped it so its visited. Helps keep track if we are immediately a winner
            self.visited.add(repr(currentState.getState()))

            if np.allclose(self.goalState.getState(), currentState.getState()):
                # We won
                print('***********end*************')
                print('visited count {0}'.format(len(self.visited)))
                print('max queue length {0}'.format(self.maxQueueLen))
                self.returnPath(currentState)
                break
            else:
                for child in self.successors(currentState):
                    # Have some children
                    if not self.check_visited(child):
                        # check in visited
                        if not self.check_queue(child):
                            # check in queue
                            if not self.heuristic:
                                # pathTree is just a reconstruction of how we got to each state so we can rebuild the final solutoion path at the end
                                # no heuristic then we dont really need to store the heuristic cost for the final path
                                self.pathTree[child] = {'parent':child.getParent(), 'cost':child.getCost(), 'direction':child.getDirection()}
                            else:
                                # otherwise we can but it doesnt really get used Im now realizing
                                self.pathTree[child] = {'parent':child.getParent(), 'cost':child.getCost(), 'direction':child.getDirection(), 'heuristic':child.get_h_cost()}
                            # append because breadth first. Use insert for depth first.
                            self.queue.append(child)
                            self.queue_track.add(repr(child.getState()))
                        else:
                            # print('found one')
                            # If the child was not in visited but was in queued then we just replace the values for the object
                            # rather than add and delete stuff
                            for q in self.queue:
                                if np.allclose(q.getState(), child.getState()):
                                    if self.heuristic == None:
                                        # no heuristic
                                        if child.getCost() < q.getCost(): #if its <= then breadth first will mess up
                                            q.setCost(child.getCost())
                                            q.setParent(child.getParent())
                                            q.setDirection(child.getDirection())
                                            self.pathTree[q] = {'parent':q.getParent(), 'cost':q.getCost(), 'direction':q.getDirection()}

                                    else:
                                        # using heuristic
                                        if child.get_h_cost() < q.get_h_cost():
                                            q.setCost(child.getCost())
                                            q.setParent(child.getParent())
                                            q.setDirection(child.getDirection())
                                            q.set_h_cost(child.get_h_cost())
                                            self.pathTree[q] = {'parent':q.getParent(), 'cost':q.getCost(), 'direction':q.getDirection(), 'heuristic':q.get_h_cost()}

    def _heuristic(self, h, state):
        # heuristic definitions are here
        s1 = state.getState()
        s2 = self.goalState.getState()
        result = 0
        # seems like I shouldnt count 0 position
        if h == Heuristic.misplaced_tiles or h == Heuristic.a_star_1:
            # Either heuristic use misplaced tiles per the assignment
            for i in range(3):
                for j in range(3):
                    if s1[i][j] != s2[i][j]:
                        result += 1
            if h == Heuristic.a_star_1:
                # this should be sum of move costs = 1 if A*1 was called with correct args
                # if it happens to be A*1 then we also add in the state cost passed in
                result += state.getCost()

        elif h == Heuristic.a_star_2:
            # Manhattan distance alone?
            result += self.sum_of_manhattan_distance(self.mD, s1, s2)

        elif h == Heuristic.a_star_3:
            # I feel like this is cheating but it works.
            # Alternative would be to assess collisions along rows and columns but I ran out of time
            result += self.sum_of_manhattan_distance(self.mD, s1, s2)+state.getCost()

        elif h == Heuristic.uniform_cost:
            result += state.getCost()

        return result

    def sum_of_manhattan_distance(self, mD, s1, s2):
        # Utility to calculate Manhattan distance
        result = 0
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
        # Instead of sorting the queue every time Im just doing a single pass and finding the lowest cost
        # then returning the IndexError
        # It does get burdensome when the queue gets long and now realizing that if I did an
        # insertion sort while putting the children into the queue I might save some time
        lowest = 0
        for i in range(len(self.queue)):
            if self.heuristic:
                if self.queue[i].get_h_cost() < self.queue[lowest].get_h_cost():
                    lowest = i
            else:
                if self.queue[i].getCost() < self.queue[lowest].getCost():
                    lowest = i
        return lowest

    def check_visited(self, child):
        # fast version because lots of checks
        # see IDS for more info
        result = False

        if repr(child.getState()) in self.visited:
            result = True
        return result

    def check_queue(self, child):
        # fast version because lots of checking
        # see IDS because my implementation kinda sucks
        result = False

        if repr(child.getState()) in self.queue_track:
            result = True
        return result

    def successors(self, root):
        # Same successor function as previous class but this time with accomodations for the heuristic costs
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

        # Doing the same thing as iterative deepening
        if zero_x != 0:
            #take left child
            leftTile = newLState[zero_x-1][zero_y]
            newLState[zero_x-1][zero_y] = 0
            newLState[zero_x][zero_y] = leftTile

            # get teh cost based on parameters passed to constructor
            cost = leftTile+root.getCost() if self.useTileWeights else 1+root.getCost()
            leftNew = State(newLState,cost,root,Direction.LEFT,depth)
            # then I get the heuristic cost based on that parameter
            # A little meta here passing itself to a function passed to a function of itself
            # probably bad practice
            leftNew.set_h_cost(self._heuristic(self.heuristic, leftNew))

            successors.append(leftNew)
            del leftNew

        # Repeat for Left, Right, Up, Down
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
        # Same as before
        steps = 0
        while self.pathTree[node]['parent']:
            steps += 1
            self.path.insert(0, {'node':node, 'data':self.pathTree[node]})
            node = self.pathTree[node]['parent']

        self.set_steps(steps)

    # Utilities below are the same as DFS and IDS
    def get_path(self):
        return self.path

    def set_steps(self, steps):
        self.steps = steps

    def get_steps(self):
        return self.steps


#----------------------------------------------------
# Had to make this separate from IDS unlike BFS variants
class solver_depthFirst:
    def __init__(self, startingState, goalState, useTileWeights):
        # Constructor
        self.visited = set()
        self.queue = []
        self.queue_track = set()
        self.pathTree = dict()
        self.path = []
        self.steps = 0
        self.queue.append(startingState)
        self.queue_track.add(repr(startingState.getState()))
        self.goalState = goalState
        self.useTileWeights = useTileWeights
        self.pathTree[startingState] = {'parent':startingState.getParent(), 'cost':startingState.getCost()}
        self.moves = 0
        self.maxQueueLen = 0

    def solve(self):
        # Solver with main loop for vanilla depth-first search
        t0 = time.time()
        while not self.is_empty(self.queue):
            # In main loop
            if time.time() - t0 > 300:
                # kill switch
                print('Queue length {0}'.format(self.maxQueueLen))
                print('visited count {0}'.format(len(self.visited)))
                print('DFS exceeded 5 minutes. Stopping')
                break

            # sanity checking
            self.moves += 1
            if self.moves%10000 == 0:
                print("Yes I'm still working current queue length: {0}".format(len(self.queue)))

            # performance reporting
            if len(self.queue) > self.maxQueueLen:
                self.maxQueueLen = len(self.queue)

            # get next on the queue
            currentState = self.queue.pop(0)
            self.queue_track.remove(repr(currentState.getState()))

            self.visited.add(repr(currentState.getState()))
            if np.allclose(self.goalState.getState(), currentState.getState()):
                # win, yay
                print('***********end*************')
                print('Queue length {0}'.format(self.maxQueueLen))
                print('visited count {0}'.format(len(self.visited)))
                self.returnPath(currentState)
                break
            else:
                # make children as previous methods do
                # then check if they are in queue and visited
                for child in self.successors(currentState):
                    if not self.check_visited(child):
                        if not self.check_queue(child):
                            #store info from when created in successor funciton.
                            self.pathTree[child] = {'parent':child.getParent(), 'cost':child.getCost(), 'direction':child.getDirection()}
                            #append because breadth first. Use insert for depth first.
                            self.queue.insert(0, child)
                            self.queue_track.add(repr(child.getState()))


    def check_visited(self, child):
        # fast version because lots of checks
        # see IDS for more info
        result = False

        if repr(child.getState()) in self.visited:
            result = True

        return result

    def check_queue(self, child):
        # fast version because lots of checking
        # see IDS because my implementation kinda sucks
        result = False

        if repr(child.getState()) in self.queue_track:
            result = True
        return result

    def successors(self, root):
        # same as before but no accomodations for heuristics
        # just vanilla DFS successor function
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

        # does the same as the others
        if zero_x != 0:
            #take left child
            leftTile = newLState[zero_x-1][zero_y]
            newLState[zero_x-1][zero_y] = 0
            newLState[zero_x][zero_y] = leftTile

            # costs are calculated and new child states created if they can be
            cost = leftTile+root.getCost() if self.useTileWeights else 1+root.getCost()
            leftNew = State(newLState,cost,root,Direction.LEFT,depth)

            successors.insert(0,leftNew)

        # repeat left, right, up, down
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
        # same as above. SOrry again for not refactoring into unified utility package
        steps = 0
        while self.pathTree[node]['parent']:
            steps += 1
            self.path.insert(0, {'node':node, 'data':self.pathTree[node]})
            node = self.pathTree[node]['parent']

        self.set_steps(steps)

    # more utilites and accessors same as above
    # getting paths and steps and checkig for empty queue
    def get_path(self):
        return self.path

    def is_empty(self,ls):
        return False if ls else True

    def set_steps(self, steps):
        self.steps = steps

    def get_steps(self):
        return self.steps


#----------------------------------------------------
class solver_iterative_deepening:
    # Just the class
    def __init__(self, startingState, goalState, useTileWeights, heuristic):
        # Constructor - I tried using this class for both iterative-deepening and
        # depth-first as I did with the BFS variants but it wasnt having it. the
        # heuristic attribute is meaningless.
        # my scope issue from BFS translated to this class may be why the attempt to double dip was messing up.
        self.visited = set()
        self.queue = []
        self.queue_track = set()
        self.pathTree = dict()
        self.path = []
        self.steps = 0
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
                # and tracking max visited because visited queued gets cleared each depth
                if self.maxVisited < len(self.visited):
                    self.maxVisited = len(self.visited)

                # sanity check
                self.moves += 1
                if self.moves%10000 == 0:
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
                # Nope, didnt win and we are still OK to keep adding to the queue
                    for child in self.successors(currentState):
                        # Have some children
                        if not self.check_visited(child):
                            # check in visited
                            if not self.check_queue(child):
                                # check in queued
                                # store info from when created in successor funciton.
                                self.pathTree[child] = {'parent':child.getParent(), 'cost':child.getCost(), 'direction':child.getDirection()}
                                # append because breadth first. Use insert for depth first.
                                self.queue.insert(0, child)
                                # queue_track doesnt need to be in order
                                self.queue_track.add(repr(child.getState()))

            if not self.win:
                self.start_again()
            else:
                break

    def start_again(self):
        # Start all the queues over
        self.reset_start_state()
        self.queue.append(self.start_state)
        self.queue_track.add(repr(self.start_state.getState()))
        self.pathTree[self.start_state] = {'parent':self.start_state.getParent(), 'cost':self.start_state.getCost()}
        current_depth = 0
        self.visited.clear()

    def reset_start_state(self):
        # Just a utility for restarting
        self.start_state.setCost(0)
        self.start_state.setDirection(None)
        self.start_state.setParent(None)
        self.start_state.set_depth(0)

    def check_visited(self, child):
        # OK so this ended up being the fastest way to determine if child was in visited
        # that my skills allowed me to implement in the time given
        result = False

        if repr(child.getState()) in self.visited:
            result = True

        return result

    def check_queue(self, child):
        # OK so this ended up being the fastest way to determine if child was in queued
        # that my skills allowed me to implement in the time given
        result = False

        if repr(child.getState()) in self.queue_track:
            result = True

        return result

    def successors(self, root):
        # Successor function if it wasnt obvious.
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

        # Just checking row or column depending on which direction to move
        # then if its ok to move in that direction do so with a simple swap
        # calculate the cost and build the new state object
        # add it to a mini queue that gets returned to the main loop
        if zero_x != 0:
            #take left child
            leftTile = newLState[zero_x-1][zero_y]
            newLState[zero_x-1][zero_y] = 0
            newLState[zero_x][zero_y] = leftTile

            cost = leftTile+root.getCost() if self.useTileWeights else 1+root.getCost()
            leftNew = State(newLState,cost,root,Direction.LEFT,depth)

            successors.insert(0,leftNew)

        # Just repeates for Left, Right, Up, Down
        # The order of this does change the runtime
        # Sort of pointless to try to order these to run faster for this particular
        # collection of start and win states though.
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
        # This or recursive, doesnt relaly matter. Just builds out the solution tree for whatever later use
        while self.pathTree[node]['parent']:
            steps += 1
            self.path.insert(0, {'node':node, 'data':self.pathTree[node]})
            node = self.pathTree[node]['parent']

        self.set_steps(steps)

    # Accessor functions
    def get_path(self):
        # Return the final path assuming it finished and could consruct the whole thing
        return self.path

    def is_empty(self,ls):
        # Utility to check queue being empty and stop main loop
        return False if ls else True

    def set_steps(self, steps):
        # Utility for counting the steps fo the final path
        self.steps = steps

    def get_steps(self):
        # Returns the steps of the final path
        return self.steps


################################################################################################################################
# Stuff to make them run

# You can just run this file and get everything. Output isnt the best.
# So my class declarations were setting up attributes with incorrect scope. I didnt notice in development
# because I was testing one instance of the algorithm at a time
# when I uncommented all of them to let them all run one after the other the double dip implementations were
# hanging on to data from previous runs. I thought I was done with this hours ago until that popped up, now Im late to submit.
# one of those cases where Python is being as annoying as javascript

easyStart = State([[1,8,7],[3,6,0],[4,2,5]],0,[],None,0)
medStart = State([[2,0,7],[8,4,6],[1,3,5]],0,[],None,0)
hardStart = State([[5,4,3],[6,0,2],[7,8,1]],0,[],None,0)
what = State([[1,7,0],[2,8,6],[3,4,5]],0,[],None,0)# for testing
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
print('\nStarting breadth-first easy')
d_solver = solver_FIFO(easyStart,winningState,True,None)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver

print('\nStarting breadth-first med')
d_solver = solver_FIFO(medStart,winningState,True,None)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver

print('\nStarting breadth-first hard')
d_solver = solver_FIFO(hardStart,winningState,True,None)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver

# # depth-first - dont use tile weights? If true it will tally but notuse them for next path to check.
print('\nStarting depth-first easy')
d_solver = solver_depthFirst(easyStart,winningState,True)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver

print('\nStarting depth-first med')
d_solver = solver_depthFirst(medStart,winningState,True)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver

print('\nStarting depth-first hard')
d_solver = solver_depthFirst(hardStart,winningState,True)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver
#
# # iterative deepening - dont use tile weights? If true it will tally but not use them for next path to check.
print('\nStarting iterative-deepening easy')
d_solver = solver_iterative_deepening(easyStart,winningState,True,Heuristic.iterative_deepening)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver

print('\nStarting iterative-deepening med')
d_solver = solver_iterative_deepening(medStart,winningState,True,Heuristic.iterative_deepening)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver

print('\nStarting iterative-deepening hard')
d_solver = solver_iterative_deepening(hardStart,winningState,True,Heuristic.iterative_deepening)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver
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
print('\nStarting best-first easy')
d_solver = solver_FIFO(easyStart,winningState,True,Heuristic.misplaced_tiles)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver

print('\nStarting best-first med')
d_solver = solver_FIFO(medStart,winningState,True,Heuristic.misplaced_tiles)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver

print('\nStarting best-first hard')
d_solver = solver_FIFO(hardStart,winningState,True,Heuristic.misplaced_tiles)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver
#
# # A*1 - do use tile weights and uses a heuristic (per assignment - other impls. just use 1 for cost)
print('\nStarting A*1 easy')
d_solver = solver_FIFO(easyStart, winningState, True, Heuristic.a_star_1)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver

print('\nStarting A*1 med')
d_solver = solver_FIFO(medStart, winningState, True, Heuristic.a_star_1)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver

print('\nStarting A*1 hard')
d_solver = solver_FIFO(hardStart, winningState, True, Heuristic.a_star_1)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver
#
# # A*2 - I think this one is purely Manhattan distance and no move cost function
print('\nStarting A*2 easy')
d_solver = solver_FIFO(easyStart, winningState, True, Heuristic.a_star_2)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver

print('\nStarting A*2 med')
d_solver = solver_FIFO(medStart, winningState, True, Heuristic.a_star_2)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver

print('\nStarting A*2 hard')
d_solver = solver_FIFO(hardStart, winningState, True, Heuristic.a_star_2)
d_solver.solve()
print_the_solution(d_solver.get_path())
print('Path steps {0}'.format(d_solver.get_steps()))
del d_solver
#
# # A*3 - Basically manhattan distance plus cost h(n)+g(n)
print('\nStarting A*3 easy')
a3easy_solver = solver_FIFO(easyStart, winningState, True, Heuristic.a_star_3)
a3easy_solver.solve()
print_the_solution(a3easy_solver.get_path())
print('Path steps {0}'.format(a3easy_solver.get_steps()))
del a3easy_solver

print('\nStarting A*3 med')
a3med_solver = solver_FIFO(medStart, winningState, True, Heuristic.a_star_3)
a3med_solver.solve()
print_the_solution(a3med_solver.get_path())
print('Path steps {0}'.format(a3med_solver.get_steps()))
del a3med_solver

print('\nStarting A*3 hard')
a3hard_solver = solver_FIFO(hardStart, winningState, True, Heuristic.a_star_3)
a3hard_solver.solve()
print_the_solution(a3hard_solver.get_path())
print('Path steps {0}'.format(a3hard_solver.get_steps()))
del a3hard_solver

class solver_breadthFirst:
    visited = []
    queue = []
    def __init__(self, startingState, goalState):
        self.queue.append(startingState)
        self.goalState = goalState

    def solve(self):
        while self.queue:
            currentState = self.queue.pop(0)
            self.visited.append(currentState)
            if np.allclose(self.goalState.getState(), currentState.getState()):
                return self.returnPath(currentState)
                break
            else:
                for child in self.successors(currentState):
                    if child not in visited:
                        if child not in queue:
                            #store info from when created in successor funciton.
                            #append because breadth first. Use insert for depth first.
                            queue.append(child)

            visited.append(currentState)

    def returnPath(self, root):
        #returns list of dicts to use to define solution. Evrything should be in visited

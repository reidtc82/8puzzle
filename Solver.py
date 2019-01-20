class solver_breadthFirst:
    # visited = []
    enqueue = []
    def __init__(self, startingState, goalState):
        self.enqueue.append(startingState)
        self.goalState = goalState

    def solve(self):
        while len(self.enqueue) > 0:
            currentState = self.enqueue.pop(0)
            if np.allclose(self.goalState.getState(), currentState.getState()):
                return {"path":currentState.getPath(), "cost":currentState.getCost()}
                break
            else:
                thisZero = currentState.getZeroLocation()

                if thisZero.col == 0:
                    #only search right
                    if thisZero.row == 0:
                        #only search down
                    else if thisZero.row == 1:
                        #search both
                    else if thisZero.row == 2:
                        #only search up
                else if thisZero.col == 1:
                    #search left and right
                else if thisZero.col == 2:
                    #only search left

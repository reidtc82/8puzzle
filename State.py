class State:
    def __init__(self, state, cost, parent):
        self.state = state
        self.cost = cost
        self.parent = parent

    def getState(self):
        return self.state

    def getCost(self):
        return self.cost

    def getParent(self):
        return self.parent

    def addCost(self, pathCost):
        self.cost += pathCost

    def addParent(self, parent):
        self.parent = parent

    def getZeroLocation(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    zero_location = {'col':i,'row':j}
        return zero_location

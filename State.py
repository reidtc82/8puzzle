class State:
    def __init__(self, state, cost, path):
        self.state = state
        self.cost = cost
        self.path = path

    def getState(self):
        return self.state

    def getCost(self):
        return self.cost

    def getPath(self):
        return self.path

    def addCost(self,pathCost):
        self.cost += pathCost

    def addPath(self,parent):
        self.path.append(parent)

    def getZeroLocation(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    zero_location = {'col':i,'row':j}
        return zero_location

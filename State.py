class State:
    def __init__(self, state):
        self.state = state
        self.cost = 0
        self.path = []

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

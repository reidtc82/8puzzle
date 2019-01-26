class State:
    def __init__(self, state, cost, parent, dir, dep):
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

    def getState(self):
        return self.state

    def getCost(self):
        return self.cost

    def getParent(self):
        return self.parent

    def setCost(self, pathCost):
        self.cost = pathCost

    def setParent(self, parent):
        self.parent = parent

    def getZeroLocation(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    zero_location = {'col':i,'row':j}
        return zero_location

    def getDirection(self):
        return self.direction

    def setDirection(self, dir):
        self.direction = dir

    def getDepth(self):
        return self.depth

    def set_depth(self, dep):
        self.depth = dep

    def set_h_cost(self, hCost):
        self.hCost = hCost

    def get_h_cost(self):
        return self.hCost

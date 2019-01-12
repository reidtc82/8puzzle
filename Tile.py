class Tile:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos

    def getPos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = pos

    def getValue(self):
        return self.value

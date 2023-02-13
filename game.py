from cell import *

class Game:
    def __init__(self, xSize=100, ySize=80, procgen=True):
        self.xSize = xSize
        self.ySize = ySize
        self.things = {}
        self.procgen = procgen
        self.screen = []
        for y in range(ySize):
            self.screen.append([])
            for x in range(xSize):
                self.screen[y].append(Cell(x, y, []))
        for i in self.screen:
            for c in i:
                print(c, end='')
            print()

    def printAsScreen(self):
        for i in self.screen:
            for c in i:
                print(c, end='')
            print()





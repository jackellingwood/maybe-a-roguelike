from thing import *

class Player(Thing):
    def __init__(self, x, y, inv, name='Bob', health=20, strength=10):
        super().__init__(x, y)
        self.symbol = '@'
        self.inv = inv
        self.name = name
        self.health = health
        self.strength = strength

    def getInv(self):
        return self.inv

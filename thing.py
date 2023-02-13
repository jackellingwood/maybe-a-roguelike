# this will be an abstract class for things in the game

#layers:
# 1 = player
# 2 = enemy
# 3 = item
# 4 = door
# 5 = wall (┌,┐,└,┘,─,│)
#    ┌─┐   ┌─┐
#    │ │   │ │
#    └─┘   └─┘
# ┌─────────────┐
# └┐           ┌┘
#  └───────────┘

class Thing:
    def __init__(self, x, y):
        self.symbol = '0'
        self.visible = True
        self.x = x
        self.y = y

    def die(self):
        del self
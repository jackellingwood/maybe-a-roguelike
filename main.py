from cell import *
from thing import *
from player import *
from game import *
game = Game()
x = 4
y = 3
game.screen[x][y].add(Player(x, y, []))
game.printAsScreen()
print(game.screen[x][y].contents[0].getInv())
# for y in range(5):
#     screen.append([])
#     for x in range(10):
#         screen[y].append(Cell(x, y, []))

# ourCell = screen[4][3]
# ourCell.add(thing(2))
# print(ourCell)
# print("    ┌─┐   ┌─┐\n    │ │   │ │\n    └─┘   └─┘\n ┌─────────────┐\n └┐           ┌┘\n  └───────────┘ ")

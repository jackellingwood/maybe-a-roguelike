#layers:
# 1 = player
# 2 = enemy
# 3 = item
# 4 = door
# 5 = wall
class Object:
    def __init__(self, layer):
        self.layer = layer
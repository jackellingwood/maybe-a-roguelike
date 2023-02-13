class Cell:

    # https://realpython.com/linked-lists-python/

    def __init__(self, x, y, contents):
        self.x = x
        self.y = y
        self.contents = contents

    def __str__(self):
        return str(self.contents)

    def add(self, thing):
        self.contents.append(thing)
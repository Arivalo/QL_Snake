import numpy as np


class Treat:
    def __init__(self, board_size):
        self.board_size = board_size
        self.color = (250, 150, 50)
        self.x = np.random.randint(0, self.board_size)
        self.y = np.random.randint(0, self.board_size)

    def change_pos(self):
        self.x = np.random.randint(0, self.board_size)
        self.y = np.random.randint(0, self.board_size)

    def __sub__(self, other):
        return other.x - self.x, other.y - self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

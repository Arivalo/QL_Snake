class Snake:
    def __init__(self, board_size):
        self.x = 8
        self.y = 7
        self.size = 4
        self.dir = 1  # directions are 0-up, 1-right, 2-down, 3-left
        self.ate = False
        self.crashed = False
        self.board_size = board_size
        self.body = []
        self.color = (255, 255, 255)
        for i in range(self.size):
            self.body.append((self.x-i, self.y-i))

    def move(self):
        if self.dir % 2 == 0:
            if self.dir > 0:
                self.y += 1
            else:
                self.y -= 1
        else:
            if self.dir > 1:
                self.x += 1
            else:
                self.x -= 1

        if self.x >= self.board_size:  # no walls, snake will go through
            self.x = 0
            self.crashed = True
        elif self.x < 0:
            self.x = self.board_size - 1
            self.crashed = True
        if self.y >= self.board_size:
            self.y = 0
            self.crashed = True
        elif self.y < 0:
            self.y = self.board_size - 1
            self.crashed = True

        if self.ate:
            self.ate = False
            self.body.append(self.body[-1])

        self.body[0] = (self.x, self.y)
        for i in range(len(self.body)):
            if i > 0:
                self.body[-i] = self.body[-i-1]

    def __sub__(self, other):
        return self.x - other.x, self.y - other.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def change_direction(self, new_dir):
        if abs(self.dir - new_dir) != 2:
            self.dir = new_dir

    def act(self, new_dir):
        if new_dir != self.dir:
            self.change_direction(new_dir)
        self.move()

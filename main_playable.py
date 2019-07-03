import numpy as np
import pygame as pg

pg.init()
clock = pg.time.Clock()

SW = 600
SH = 600

win = pg.display.set_mode((SW, SH))

SIZE = 15
SCALING = SW//SIZE


class Snake:
    def __init__(self):
        self.x = 8
        self.y = 7
        self.size = 3
        self.dir = 1  # directions are 0-up, 1-right, 2-down, 3-left
        self.ate = False
        self.body = []
        for i in range(self.size):
            self.body.append((self.x - i, self.y - i))

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

        if self.x >= SIZE:  # no walls, snake will go through
            self.x = 0
        elif self.x < 0:
            self.x = SIZE - 1
        if self.y >= SIZE:
            self.y = 0
        elif self.y < 0:
            self.y = SIZE - 1

        if self.ate:
            self.ate = False
            self.body.append(self.body[-1])

        self.body[0] = (self.x, self.y)
        for i in range(len(self.body)):
            if i > 0:
                self.body[-i] = self.body[-i - 1]

    def change_direction(self, new_dir):
        if abs(self.dir - new_dir) != 2:
            self.dir = new_dir

    def act(self, new_dir):
        if new_dir != self.dir: self.change_direction(new_dir)

    def draw(self, window):
        for part in self.body:
            pg.draw.rect(window, (255, 255, 255),
                         (part[0] * SCALING + 1, part[1] * SCALING + 1, SCALING - 2, SCALING - 2))


class Treat:
    def __init__(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)

    def change_pos(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)

    def draw(self, window):
        pg.draw.rect(window, (0, 255, 100), (self.x * SCALING, self.y * SCALING, SCALING, SCALING))


run = True
mainSnake = Snake()
food = Treat()

while run:
    clock.tick(15)

    inputs = pg.key.get_pressed()

    if inputs[pg.K_UP]:
        mainSnake.act(0)
    elif inputs[pg.K_DOWN]:
        mainSnake.act(2)
    elif inputs[pg.K_RIGHT]:
        mainSnake.act(3)
    elif inputs[pg.K_LEFT]:
        mainSnake.act(1)

    mainSnake.move()

    for part in mainSnake.body:
        if part == (mainSnake.x, mainSnake.y) and part is not mainSnake.body[0]:
            run = False

    if mainSnake.x == food.x and mainSnake.y == food.y:
        mainSnake.ate = True
        food.change_pos()
        inside = False
        for part in mainSnake.body:
            if part == (food.x, food.y):
                inside = True
                break
        while inside:
            inside = False
            food.change_pos()
            for part in mainSnake.body:
                if part == (food.x, food.y):
                    inside = True
                    break

    pg.draw.rect(win, (0, 0, 0), (0, 0, SW, SH))
    mainSnake.draw(win)
    food.draw(win)
    pg.display.update()

    for event in pg.event.get():
        if event.type is pg.QUIT:
            run = False

pg.quit()
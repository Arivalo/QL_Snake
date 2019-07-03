import numpy as np
import pickle
import pygame as pg

SIZE = 15
EPOCHS = 100000
LOSE_PENALTY = 200
EAT_REWARD = 35
MOVE_PENALTY = 3
EPS = 0.9
EPS_DECAY = 0.999
SHOW_WHEN = 5000
LEARNING_RATE = 0.1
DISCOUNT = 0.98
SNAKE_KEY = 1
FOOD_KEY = 2

starting_q_table = None

colours = {1: (255,255,255), 2: (100,255,1000)}

class Snake:
    def __init__(self):
        self.x = 8
        self.y = 7
        self.size = 3
        self.dir = 1 # directions are 0-up, 1-right, 2-down, 3-left
        self.ate = False
        self.body = []
        for i in range(self.size):
            self.body.append((self.x-i, self.y-i))

    def move(self, new_dir):
        if self.dir%2 == 0:
            if self.dir > 0:
                self.y += 1
            else:
                self.y -= 1
        else:
            if self.dir > 1:
                self.x += 1
            else:
                self.x -= 1

        if self.x >= SIZE: # no walls, snake will go through
            self.x = 0
        elif self.x < 0:
            self.x = SIZE-1
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
                self.body[-i] = self.body [-i-1]

    def change_direction(self, new_dir):
        if abs(self.dir - new_dir) != 2:
            self.dir = new_dir

class Treat:
    def __init__(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)

    def change_pos(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)
#==========================================================================#

# observation space is location of food relative to head and is there a body on the left, right or fowards
if starting_q_table is None:
    q_table = {}
    for xtf in range(-SIZE+1, SIZE):
        for ytf in range(-SIZE+1, SIZE):
            for lb in range(2): 
                for rb in range(2):
                    for ub in range(2):
                        for db in range(2):
                            for direction in range(4):
                                q_table[(xtf, ytf), lb, rb, ub, db, direction] = np.random.uniform(-8, 0, size=4)
else:
    with open(starting_q_table, "rb") as f:
        q_table = pickle.load(f)

epoch_rewards

for epoch in range(EPOCHS):
    python = Snake()
    food = Treat()
    
    if epoch % SHOW_WHEN:
        render = True
        print(f"#{epoch}, mean: {np.mean(episode_rewards[-SHOW_WHEN:])}")   
    else:
        render = False

    epoch_rew = 0
    for i in range(100+epoch):
        left_b = 0
        right_b = 0
        up_b = 0
        down_b = 0
        for part in python.body:
            if part == (python.x - 1, python.y): left_b = 1       ######## add beyond wall #######                        
            if part == (python.x + 1, python.y): right_b = 1
            if part == (python.x, python.y - 1): up_b = 1
            if part == (python.x, python.y + 1): down_b = 1
 
        obs = ((python.x-food.x,python.y-food.y), left_b, right_b, up_b, down_b, python.dir)
        
        if np.random.random() > EPS:
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0,4)

        python.change_direction(action)


            

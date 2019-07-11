#import pygame as pg
from PIL import Image
import numpy as np
from snake_object import Snake
from food_object import Treat
import cv2

class SnakeEnvObject:
    SW = 600
    SIZE = 15
    WALLS = True
    LOSE_PENALTY = 601
    EAT_REWARD = 60
    MOVE_PENALTY = 3
    ACTION_SPACE_SIZE = 4
    OBSERVATION_SPACE_VALUES = (SIZE, SIZE, 3)
    FPS = 30
    SCALING = SW // SIZE
    RETURN_IMAGES = True # change depending on whether you use neural network or simple QL

    def reset(self):
        self.player = Snake(self.SIZE)
        self.food = Treat(self.SIZE)
        inside = False
        for part in self.player.body:
            if part == (self.food.x, self.food.y):
                inside = True
                break
        while inside:
            inside = False
            self.food.change_pos()
            for part in self.player.body:
                if part == (self.food.x, self.food.y):
                    inside = True
                    break

        self.episode_step = 0
        observation = self.get_observation()

        return observation

    def get_observation(self):

        if self.RETURN_IMAGES:
            observation = np.array(self.get_image())
        else:
            left_b = 0  # is there a part of snake or wall (if turned on) on the left
            right_b = 0  # same on right
            up_b = 0   # same but a grid up
            down_b = 0  # same but a grid down
            for part in self.player.body:
                if part == (self.player.x - 1, self.player.y):
                    left_b = 1
                elif self.player.x - 1 < 0 and part == (self.SIZE-1, self.player.y):
                    left_b = 1
                if part == ((self.player.x + 1) % self.SIZE, self.player.y):
                    right_b = 1
                if part == (self.player.x, self.player.y - 1):
                    up_b = 1
                elif self.player.y - 1 < 0 and part == (self.player.x, self.SIZE-1):
                    up_b = 1
                if part == (self.player.x, (self.player.y + 1) % self.SIZE):
                    down_b = 1

            if self.WALLS:
                if self.player.x == 0:
                    left_b = 1
                if self.player.x == self.SIZE-1:
                    right_b = 1
                if self.player.y == 0:
                    up_b = 1
                if self.player.x == self.SIZE-1:
                    down_b = 1

            # observation contains: tuple of relative coordinates of snake to food, walls or body parts
            # in all directions and current snake direction
            observation = ((self.player-self.food), left_b, right_b, up_b, down_b, self.player.dir)

        return observation

    def step(self, action):
        self.episode_step += 1
        self.player.act(action)

        new_observation = self.get_observation()

        # if walls are turned on
        if self.WALLS and self.player.crashed:
            reward = -self.LOSE_PENALTY
            done = True
        # if snake is at the same grid as food
        elif self.player == self.food:
            self.player.ate = True
            self.food.change_pos()
            done = False
            inside = False
            for part in self.player.body:
                if part == (self.food.x, self.food.y):
                    inside = True
                    break
            while inside:
                inside = False
                self.food.change_pos()
                for part in self.player.body:
                    if part == (self.food.x, self.food.y):
                        inside = True
                        break
            reward = self.EAT_REWARD
        # otherwise its either normal move or snake hit itself
        else:
            reward = 0
            done = False
            for part in self.player.body:
                if part == (self.player.x, self.player.y) and part is not self.player.body[0]:
                    done = True
                    reward = -self.LOSE_PENALTY
                    break
            if reward == 0:
                reward = -self.MOVE_PENALTY

        return new_observation, reward, done

    def render(self):
        img = self.get_image()
        img = img.resize((300, 300))
        cv2.imshow("image", np.array(img))
        cv2.waitKey(30)
        '''pg.init()
        clock = pg.time.Clock()
        win = pg.display.set_mode((self.SW, self.SW))
        clock.tick(self.FPS)
        win.fill((0,0,0))
        for part in self.player.body:
            pg.draw.rect(win, self.player.color,
                         (part[0] * self.SCALING + 1, part[1] * self.SCALING + 1, self.SCALING - 2, self.SCALING - 2))

        pg.draw.rect(win, self.food.color,
                     (self.food.x * self.SCALING, self.food.y * self.SCALING, self.SCALING, self.SCALING))

        pg.display.update()'''

    def get_image(self):
        env = np.zeros((self.SIZE, self.SIZE, 3), dtype=np.uint8)
        for part in self.player.body:
            env[part[0]][part[1]] = self.player.color
        env[self.player.x][self.player.y] = (100, 200, 200)
        env[self.food.x][self.food.y] = self.food.color
        img = Image.fromarray(env, 'RGB')
        return img

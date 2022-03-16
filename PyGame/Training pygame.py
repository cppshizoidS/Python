import pygame
from pygame.locals import *
import numpy as np

W = 400
H = 200
max_fire = 195
interp_method = 0


def calc_palette():
    clrs = np.array([[0, 0, 0],
                     [180, 25, 25],
                     [230, 128, 25],
                     [230, 230, 25],
                     [245, 245, 163]])
    r = np.interp(np.linspace(0, 1, max_fire), [0, 0.25, 0.5, 0.75, 1], clrs[:, 0])
    g = np.interp(np.linspace(0, 1, max_fire), [0, 0.25, 0.5, 0.75, 1], clrs[:, 1])
    b = np.interp(np.linspace(0, 1, max_fire), [0, 0.25, 0.5, 0.75, 1], clrs[:, 2])
    return np.reshape(np.dstack((r, g, b)), [max_fire, 3]).astype(int)


palette = calc_palette()


def recalc_fire(field):
    field[:, :-1] += field[:, 1:]
    field = field // 2
    field[field > max_fire] = max_fire
    return field.astype(int)


def draw_fire(field, surface):
    clrs = field.copy()
    clrs[1:] += field[:-1]
    clrs[:-1] += field[1:]
    clrs[:, 1:] += field[:, :-1]
    clrs[:, :-1] += field[:, 1:]
    clrs = clrs // 5
    clrs[clrs >= max_fire] = max_fire - 1
    clrs = palette[clrs]
    pygame.surfarray.blit_array(surface, clrs)
    return surface, clrs


class flame:
    def __init__(self, max_step, min_flame, max_flame, x):
        self.step = 0
        self.max_step = max_step
        self.min_flame = min_flame
        self.max_flame = max_flame
        self.x = np.array(x, dtype=int)
        self.y1 = np.zeros([x[-1] - x[0]], dtype=int)
        self.dy = np.zeros([x[-1] - x[0]], dtype=int)
        self.__recreate__()
        self.recalc()

    def __recreate__(self):
        self.y1 += self.dy
        r = np.random
        y = r.randint(self.min_flame, self.max_flame, [len(self.x)], dtype=int)
        y = np.interp(np.arange(self.x[0], self.x[-1]), self.x, y).astype(int)
        self.dy = (y - self.y1).astype(int)

    def recalc(self):
        x = [0, self.max_step]
        fx = [self.step]
        self.fy = (self.y1 + (self.dy * self.step / self.max_step)).astype(int)
        self.step += 1
        if self.step == self.max_step:
            self.__recreate__()
            self.step = 0

    def add_flame(self, field):
        field[self.x[0]:self.x[-1], -1] += self.fy
        field[field > max_fire] = max_fire
        return field


field = np.zeros([W, H], dtype=int)
fs = [flame(40, 0, 60, np.linspace(0, 400, 51, dtype=int)),
      flame(20, 0, 30, np.linspace(0, 400, 101, dtype=int)),
      flame(10, 0, 20, np.linspace(0, 400, 201, dtype=int))]
screen = pygame.display.set_mode((W, H))
flag = 1
while flag:
    field = recalc_fire(field)
    for f in fs:
        field = f.add_flame(field)
        f.recalc()
    screen, clrs = draw_fire(field, screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = 0
pygame.quit()

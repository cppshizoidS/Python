from random import randint
import pygame
import time
from math import ceil

size = 50
X, Y = 800, 600
N, M = X//2//size+1, 2*Y//size+1
dx, dy = X//2, -N*size//2
max_h = size*1.5

def pos(x, y, h=0):
    return (x-y)*size+dx, (x+y)*size//2-h+dy

class prizm:
    def __init__(self, x, y, h, hh):
        self.x = x
        self.y = y
        self.h = h
        self.hh = hh
    
    def tick_h(self):
        if self.h == self.hh:
            self.hh = randint(0, max_h)
        if self.h > self.hh:
            self.h -= 1
        else:
            self.h += 1

    def draw(self, surface):
        x, y, h = self.x, self.y, self.h
        p = [pos(x, y, 0), pos(x, y-1, 0), pos(x, y-1, h), pos(x, y, h)]
        pygame.draw.polygon(surface, [64, 64, 64], p)
        p = [pos(x, y, 0), pos(x-1, y, 0), pos(x-1, y, h), pos(x, y, h)]
        pygame.draw.polygon(surface, [192, 192, 192], p)
        p = [pos(x, y, h), pos(x-1, y, h), pos(x-1, y-1, h), pos(x, y-1, h)]
        pygame.draw.polygon(surface, [128, 128, 128], p)

screen = pygame.display.set_mode((X, Y))
surf = pygame.Surface((X, Y))
n, m = N, M
dn, dm = -1, -1
s = n+m
a = []
for i in range(s):
    a += [prizm(i, j, 0, 0) for j in range(n, s-m+1)]
    n += dn
    m += dm
    if n == 0:
        dn = 1
    if m == 0:
        dm = 1

def tick_color(clr, d):
    for i in range(3):
        clr[i] += d[i]
    if clr == [255, 0, 0]:
        d = [0, 1, 0]
    elif clr == [255, 255,0]:
        d = [-1, 0, 0]
    elif clr == [0, 255, 0]:
        d = [0, 0, 1]
    elif clr == [0, 255, 255]:
        d = [0, -1, 0]
    elif clr == [0, 0, 255]:
        d = [1, 0, 0]
    elif clr == [255, 0, 255]:
        d = [0, 0, -1]
    return clr, d

flag = 1
clr = [255, 0, 0]
d = [0, 1, 0]
clock = pygame.time.Clock()
while flag:
    clr, d = tick_color(clr, d)
    screen.fill(clr)
    for i in a:
        i.tick_h()
        i.draw(surf)
    screen.blit(surf, (0,0), special_flags = pygame.BLEND_MIN)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            flag = 0
    clock.tick(60)
pygame.quit()

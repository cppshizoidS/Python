import pygame
from pygame.locals import *
from math import *
from random import randint
import time

W = 1366
H = 768
PI_HALF = pi / 2
ANGLE_X = radians(140)
ANGLE_Y = radians(120)
FOW_X = pi / ANGLE_X
FOW_Y = pi / ANGLE_Y
W_CENTER = W / 2 * (1 - FOW_X)
H_CENTER = H / 2 * (1 - FOW_Y)
W_PI = W / pi * FOW_X
H_PI = H / pi * FOW_Y
MAX_HYP = 500
MAX_STARS = 1500
FLAGS = FULLSCREEN
MAX_FRAMES = 0

acot = lambda x: PI_HALF - atan(x)
hypot1 = lambda x, y, z: sqrt(x*x + y*y + z*z)

def is_in_fow(x, angle):
    if (pi - angle) / 2 <= PI_HALF - abs(PI_HALF - x):
        return True
    else:
        return False

class star:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.set_pos2()
    
    def set_pos2(self):
        if self.z != 0:
            x_angle = acot(-self.x / self.z)
            y_angle = acot(self.y / self.z)
            if is_in_fow(x_angle, ANGLE_X) and is_in_fow(y_angle, ANGLE_Y):
                self.x2 = int((x_angle * W_PI) + W_CENTER)
                self.y2 = int((y_angle * H_PI) + H_CENTER)
            else:
                self.x2 = None
                self.y2 = None
    
    def draw(self, surface):
        if (self.x2 != None) and (self.y2 != None):
            hyp = hypot1(self.x, self.y, self.z)
            if hyp <= MAX_HYP:
                clr = [255 * (1 - hyp/MAX_HYP) for i in range(3)]
                pos = (self.x2, self.y2)
                pygame.draw.line(surface, clr, pos, pos)
    
    def move(self, dx, dy, dz):
        self.x += dx
        self.y += dy
        self.z += dz
        self.set_pos2()

r = range(MAX_STARS)
a = [star(randint(-200, 200), randint(-200, 200), randint(1, 500)) for i in r]

pygame.init()
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 10)

screen = pygame.display.set_mode((W, H), FLAGS)
timer = pygame.time.Clock()
flag = True
while flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            flag = False
    screen.fill((0, 0, 0))
    for j in a:
        j.draw(screen)
    timer.tick(MAX_FRAMES)
    text = font.render('FPS: %d' % int(timer.get_fps()), True, (255, 255, 0))
    screen.blit(text, text.get_rect())
    pygame.display.flip()
    for j in r:
        a[j].move(0, 0, -1)
        if a[j].z <= 0:
            a[j] = star(randint(-200, 200), randint(-200, 200), 500)

pygame.quit()

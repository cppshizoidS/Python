import pygame, random, time
from pygame.locals import *

MIN = 10
MAX = 50
WIDTH = 640
HEIGHT = 480
LINELEN = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FRAMES = 200
SLEEPTIME = 1 / FRAMES

def start():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Rain')
    global arr
    arr = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for i in range(MAX)]
    background = make_background()
    return None

def make_background():
    for y in range(HEIGHT):
        color = [int(255 * (1 - (y / 480))) for i in range(3)]
        pygame.draw.line(screen, color, (0, y), (640, y))
    global background
    background = pygame.surfarray.array2d(screen)
    return None

def movelines():
    global arr
    for i in reversed(range(len(arr))):
        arr[i][1] += 1
        if arr[i][1] - LINELEN >= HEIGHT:
            del arr[i]
    return None

def addlines():
    global arr
    for i in range(random.randint(MIN, MAX) - len(arr)):
            arr.append([random.randint(0, WIDTH), 0])
    return None

def redraw():
    global arr, screen, background
    pygame.surfarray.blit_array(screen, background)
    for i in arr:
        color = [int(255 * (i[1] / (HEIGHT + LINELEN))) for j in range(3)]
        pygame.draw.line(screen, color, i, (i[0], i[1] - LINELEN))
    pygame.display.flip()
    return None

def sleep():
    time.sleep(SLEEPTIME - time.time() % SLEEPTIME)
    return None

start()
flag = False
while not flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = True
    movelines()
    addlines()
    redraw()
    sleep()

pygame.display.quit()
pygame.quit()

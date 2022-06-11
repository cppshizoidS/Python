import os
import random
from math import dist, copysign

import pygame
from pygame.locals import *

pygame.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = '920,30'
WIDTH, HEIGHT = 1000, 1010
display = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 100)

score_sound = pygame.mixer.Sound('sounds/score.mp3')
score_sound.set_volume(0.3)
punch_sound = pygame.mixer.Sound('sounds/punch.mp3')
punch_sound.set_volume(0.1)
jump_sound = pygame.mixer.Sound('sounds/jump.mp3')
jump_sound.set_volume(0.3)

FPS = 60
clock = pygame.time.Clock()

BLUE = (30, 144, 255)
WHITE = (255, 255, 255)

PIPE_GAP = 300
GRAVITY = 0.6
JUMP_VELOCITY = 15


class EdgesMixin:

	@property
	def x(self):
		return self.rect[0]

	@property
	def y(self):
		return self.rect[1]

	@property
	def w(self):
		return self.rect[2]

	@property
	def h(self):
		return self.rect[3]
	


class BirdSprite(EdgesMixin, pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load('images/bird.png')
		self.image.set_colorkey(WHITE)
		self.image.convert_alpha()
		self.bird_image = pygame.image.load('images/bird.png')
		self.bird_image.set_colorkey(WHITE)
		self.bird_image.convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (100, HEIGHT // 2)

		self.velocity = 0
		self.degree = 0

	def draw(self, surface):
		surface.blit(self.image, self.rect)

	def collide(self, pipe: 'Pipe'):
		return (
			pygame.sprite.collide_mask(self, pipe.top) or 
			pygame.sprite.collide_mask(self, pipe.bot)
		)


class PipeSprite(EdgesMixin, pygame.sprite.Sprite):
	def __init__(self, side: str, padding: int, from_right: int = 0):
		super().__init__()
		self.image = pygame.image.load(f'images/{side}_pipe.png')
		self.image.set_colorkey(WHITE)
		self.image.convert_alpha()
		self.rect = self.image.get_rect()

		width = WIDTH + self.w // 2 - from_right
		if side == 'top':
			height = -padding + self.h // 2 - PIPE_GAP
		else:
			height = HEIGHT - padding - self.h // 2 + PIPE_GAP
		self.rect.center = (width, height)

	def draw(self, surface):
		surface.blit(self.image, self.rect)


class Pipe:
	def __init__(self, top_pipe, bottom_pipe, y_delta=0):
		self.top = top_pipe
		self.bot = bottom_pipe
		self.y_delta = y_delta


def create_pipe(from_right=0):
	padding = random.randint(-100, 100)
	top_pipe = PipeSprite('top', padding, from_right)
	bottom_pipe = PipeSprite('bottom', padding, from_right)

	y_delta = 0 if score <= 3 else random.randint(2, 4)
	y_delta = random.choice([y_delta, -y_delta])

	return Pipe(top_pipe, bottom_pipe, y_delta)


score = 0
bird = BirdSprite()
pipes = [create_pipe(400)]
pipe_to_right = pipes[0]

game_on = False
init = True
jump_freeze = False

while True:
	pressed = pygame.key.get_pressed()

	if game_on or init:
		display.fill(BLUE)

		if pipe_to_right.top.x < bird.x:
			score_sound.play()
			score += 1
			pipe_to_right = pipes[1]

		if pipes[0].top.x + pipes[0].top.w < 0:
			pipes.pop(0)

		if pipes[-1].top.x == 400:
			pipes.append(create_pipe())

		for pipe in pipes:
			if (
					pipe.top.y + pipe.top.h < 100 or
					pipe.bot.y > HEIGHT - 100
			):
				pipe.y_delta *= -1	
			pipe.top.rect.move_ip(-5, pipe.y_delta)
			pipe.bot.rect.move_ip(-5, pipe.y_delta)
			pipe.top.draw(display)
			pipe.bot.draw(display)

		if not init:
			if pressed[K_SPACE] and not jump_freeze:
				jump_sound.play()
				bird.velocity = JUMP_VELOCITY
				jump_freeze = True
			bird.velocity -= GRAVITY
			prev_y = bird.y
			bird.rect.move_ip(0, -bird.velocity)

			y_diff = prev_y - bird.y
			rot = (
				(max(min(y_diff, JUMP_VELOCITY), -JUMP_VELOCITY) + JUMP_VELOCITY) / 
				(JUMP_VELOCITY * 2)
			)
			new_degree = 160 * rot - 70
			degree_diff = dist((bird.degree, ), (new_degree, ))
			new_degree = bird.degree + copysign(
				min(40, abs(degree_diff)),
				new_degree - bird.degree,
			)
			bird.image = pygame.transform.rotate(bird.bird_image, new_degree)
			bird.degree = new_degree

			if (
					bird.y <= 0 or bird.y >= HEIGHT - bird.h or 
					bird.collide(pipes[0])
			):
				punch_sound.play()
				game_on = False

		bird.draw(display)

		image = font.render(str(score), True, WHITE)
		display.blit(image, (20, 20))

	if pressed[K_SPACE] and not game_on:
		game_on = True
		score = 0
		bird = BirdSprite()
		if len(pipes) != 1:
			pipes = [create_pipe(400)]
			pipe_to_right = pipes[0]

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
			jump_freeze = False

	pygame.display.update()
	clock.tick(FPS)

	init = False

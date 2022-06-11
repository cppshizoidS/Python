import os
import time
import random

import pygame
from pygame.locals import *


def load_image(file_name, convert_alpha=False):
	image = pygame.image.load(f'images/{file_name}')
	if convert_alpha:
		image.set_colorkey(image.get_at((0, 0)))
		image.convert_alpha()

	return image


def get_neighbours(cord, ignore_four):
	for delta_y, delta_x in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
		new_y, new_x = cord[0] + delta_y, cord[1] + delta_x
		if (
				0 <= new_y < len(tiles) and
				0 <= new_x < len(tiles[0]) and
				tiles[new_y][new_x] != 3 and
				(ignore_four or tiles[new_y][new_x] != 4)
		):
			yield new_y, new_x


def get_shortest_path(paths, end, seen=None, ignore_four=False):
	if seen is None:
		seen = set()

	new_paths = []
	for path in paths:
		for neighbour in get_neighbours(path[-1], ignore_four):
			if neighbour in seen:
				continue
			if neighbour == end:
				return path + [neighbour]
			new_paths.append(path + [neighbour])
			seen.add(neighbour)

	if not new_paths:
		return False
	return get_shortest_path(new_paths, end, seen, ignore_four)


class Entity(pygame.sprite.Sprite):

	def __init__(self, target=None):
		self.target = target

		self.facing = 'R'
		self.next_facing = None
		self.speed = 4  # px
		self.wall = {3, 4}
		self.dead = False
		self.god_mode = False
		self.god_mode_till = None
		self.scared = False
		self.spawn_tile = (10, 11)

		self.image_sets = {}
		self.facing_to_images = None
		self.images = None
		self.image = None
		self.rect = None
		self.rendered_first_cycle = False
		self.stuck = False

		self.frames_per_image = 6
		self.frame_idx = 0

		self.n_images = None
		self.image_idx = 0

	def add_images(self, name, file_name, n_images, image_order=None):
		raw_images = load_image(file_name, True)

		*_, width, height = raw_images.get_rect()
		gap = (width - height * n_images) // (n_images - 1)

		images = [
			raw_images.subsurface((height + gap) * idx, 0, height, height)
			for idx in range(n_images)
		]
		if image_order:
			image_frames = len(images) // len(image_order)
			facing_to_images = {
				direction: images[idx: idx+image_frames]
				for direction, idx in zip(
					image_order, range(0, n_images, n_images // len(image_order))
				)
			}
		else:
			image_frames = len(images)
			facing_to_images = None

		self.image_sets[name] = images, facing_to_images, image_frames

	def set_images(self, name):
		self.images, self.facing_to_images, self.n_images = self.image_sets[name]
		self.image = self.images[0]
		self.frame_idx = 0
		self.image_idx = 0
		self.rendered_first_cycle = False

	def set_rect(self, x_tile, y_tile):
		self.rect = self.image.get_rect()
		self.rect.center = (
			TILE_WIDTH * x_tile + 22,  # map border has 22px
			TILE_HEIGHT * y_tile + 22,
		)

	def draw(self, surface):
		if not self.stuck or self.dead:
			self.frame_idx += 1
		if self.frame_idx == self.frames_per_image:
			self.frame_idx = 0
			self.image_idx += 1

		if self.image_idx == self.n_images:
			self.rendered_first_cycle = True
			self.image_idx = 0

		if self.facing_to_images is not None:
			self.image = self.facing_to_images[self.facing][self.image_idx]
		else:
			self.image = self.images[self.image_idx]

		if self.rect[0] + self.rect[2] >= WIDTH:
			self.rect[0] += self.rect[2] - WIDTH
		elif self.rect[0] < 0:
			self.rect[0] += WIDTH - self.rect[2]

		surface.blit(self.image, self.rect)

	@property
	def left_top(self):
		return self.rect[0] + 4, self.rect[1] + 4

	@property
	def left_top_tile(self):
		x, y = self.left_top
		return y // TILE_HEIGHT, x // TILE_WIDTH

	@property
	def middle_cord(self):
		return self.rect[0] + 24, self.rect[1] + 24

	@property
	def middle_tile(self):
		x, y = self.middle_cord
		return y // TILE_HEIGHT, x // TILE_WIDTH

	@property
	def right_bottom(self):
		return self.rect[0] + 43, self.rect[1] + 43

	@property
	def right_bottom_tile(self):
		x, y = self.right_bottom
		return y // TILE_HEIGHT, x // TILE_WIDTH

	@property
	def ignore_four(self):
		return 4 not in self.wall

	def move_or_turn(self):
		x, y = self.left_top
		if x % TILE_WIDTH == 0 and y % TILE_HEIGHT == 0:
			available_directions = [
				direction for direction in ['R', 'L', 'U', 'D']
				if self.can_move_towards(direction, True)
			]
			current_tile = self.middle_tile
			target_tile = self.target.middle_tile

			if self.dead and current_tile == self.spawn_tile:
				self.dead = False
				self.scared = False
				self.set_images('alive')
				self.speed = 4

			if self.dead:
				target_tile = self.spawn_tile
				path = get_shortest_path(
					[[current_tile]],
					target_tile,
					ignore_four=self.ignore_four,
				)
				direction = self.get_direction(current_tile, path[1])
				self.facing = direction
			else:
				if random.random() > 0.2:
					path = get_shortest_path(
						[[current_tile]],
						target_tile,
						ignore_four=self.ignore_four,
					)
					if path:
						direction = self.get_direction(current_tile, path[1])
						if not self.scared:
							self.facing = direction
						else:
							available_directions.remove(direction)
							self.facing = random.choice(available_directions)
					else:
						self.facing = random.choice(available_directions)
				else:
					self.facing = random.choice(available_directions)

		self.move()

	@staticmethod
	def get_direction(tile_from, tile_to):
		if tile_from[0] < tile_to[0]:
			return 'D'
		elif tile_from[0] > tile_to[0]:
			return 'U'
		elif tile_from[1] < tile_to[1]:
			return 'R'
		elif tile_from[1] > tile_to[1]:
			return 'L'

	def can_move_towards(self, direction, turning=False):
		x, y = self.left_top
		if not turning or (y % TILE_HEIGHT == 0 and x % TILE_WIDTH == 0):
			if direction == 'R':
				y_tile, x_tile = self.left_top_tile
				return tiles[y_tile][x_tile + 1] not in self.wall
			elif direction == 'L':
				y_tile, x_tile = self.right_bottom_tile
				return tiles[y_tile][x_tile - 1] not in self.wall
			elif direction == 'U':
				y_tile, x_tile = self.right_bottom_tile
				return tiles[y_tile - 1][x_tile] not in self.wall
			elif direction == 'D':
				y_tile, x_tile = self.left_top_tile
				return tiles[y_tile + 1][x_tile] not in self.wall

		return False

	def move(self):
		self.stuck = False
		if not self.can_move_towards(self.facing):
			self.stuck = True
			return False

		if self.facing == 'R':
			self.rect.move_ip(self.speed, 0)
		elif self.facing == 'L':
			self.rect.move_ip(-self.speed, 0)
		if self.facing == 'U':
			self.rect.move_ip(0, -self.speed)
		elif self.facing == 'D':
			self.rect.move_ip(0, self.speed)

	def does_collide(self, sprite):
		return pygame.sprite.collide_mask(self, sprite)


class SmallDot(pygame.sprite.Sprite):

	def __init__(self):
		self.image = load_image('dot.png', True).subsurface(0, 0, 30, 30)
		self.rect = self.image.get_rect()
		self.rect.center = (45, 45)

	def draw(self, surface, cord):
		self.rect.center = cord
		surface.blit(self.image, self.rect)


class BigDot(pygame.sprite.Sprite):

	def __init__(self):
		self.image = load_image('dot.png', True).subsurface(30, 0, 40, 30)
		self.rect = self.image.get_rect()
		self.rect.center = (45, 45)

		self.frames_per_image = 30
		self.frame_idx = 0
		self.show_image = True

	def draw(self, surface, cord):
		self.frame_idx += 1
		if self.frame_idx > self.frames_per_image:
			self.frame_idx = 0
			self.show_image = not self.show_image

		if self.show_image:
			self.rect.center = cord
			surface.blit(self.image, self.rect)


os.environ['SDL_VIDEO_WINDOW_POS'] = '1080,30'
pygame.init()

map_image = load_image('map.png')
_, _, WIDTH, HEIGHT = map_image.get_rect()

display = pygame.display.set_mode((WIDTH, HEIGHT))
# 0 - empty, 1 - small_dot, 2 - big_dot, 3 - wall, 4 - pink wall
tiles = [
	[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
	[3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
	[3, 2, 3, 3, 3, 1, 3, 3, 3, 1, 3, 1, 3, 3, 3, 1, 3, 3, 3, 2, 3],
	[3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3],
	[3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
	[3, 1, 3, 3, 3, 1, 3, 1, 3, 3, 3, 3, 3, 1, 3, 1, 3, 3, 3, 1, 3],
	[3, 1, 3, 3, 3, 1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1, 3, 3, 3, 1, 3],
	[3, 1, 1, 1, 1, 1, 3, 3, 3, 0, 3, 0, 3, 3, 3, 1, 1, 1, 1, 1, 3],
	[3, 3, 3, 3, 3, 1, 3, 0, 0, 0, 0, 0, 0, 0, 3, 1, 3, 3, 3, 3, 3],
	[3, 3, 3, 3, 3, 1, 3, 0, 3, 4, 4, 4, 3, 0, 3, 1, 3, 3, 3, 3, 3],
	[3, 3, 3, 3, 3, 1, 3, 0, 3, 0, 0, 0, 3, 0, 3, 1, 3, 3, 3, 3, 3],
	[0, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0],
	[3, 3, 3, 3, 3, 1, 3, 0, 3, 3, 3, 3, 3, 0, 3, 1, 3, 3, 3, 3, 3],
	[3, 3, 3, 3, 3, 1, 3, 0, 0, 0, 0, 0, 0, 0, 3, 1, 3, 3, 3, 3, 3],
	[3, 3, 3, 3, 3, 1, 3, 0, 3, 3, 3, 3, 3, 0, 3, 1, 3, 3, 3, 3, 3],
	[3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
	[3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3],
	[3, 2, 1, 1, 3, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 3, 1, 1, 2, 3],
	[3, 3, 3, 1, 3, 1, 3, 1, 3, 3, 3, 3, 3, 1, 3, 1, 3, 1, 3, 3, 3],
	[3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3],
	[3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 3],
	[3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 3],
	[3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
	[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]
TILE_WIDTH, TILE_HEIGHT = WIDTH // len(tiles[0]), HEIGHT // len(tiles)

FPS = 60
clock = pygame.time.Clock()

pac_man = Entity()
pac_man.add_images('alive', 'pac_man.png', 8, ('R', 'U', 'L', 'D'))
pac_man.add_images('death', 'pac_man_death.png', 12)
pac_man.set_images('alive')
pac_man.set_rect(10, 17)

enemies = {}
enemies_names = ['blinky', 'clyde', 'inky', 'pinky']
for enemy_name in enemies_names:
	enemies[enemy_name] = Entity(pac_man)
	enemies[enemy_name].add_images('alive', f'{enemy_name}.png', 8, ('R', 'L', 'U', 'D'))
	enemies[enemy_name].add_images('scared', 'ghost_scared.png', 2)
	enemies[enemy_name].add_images('eyes', 'ghost_eyes.png', 4, ('R', 'L', 'U', 'D'))
	enemies[enemy_name].set_images('alive')
	enemies[enemy_name].set_rect(10, 11)

small_dot = SmallDot()
big_dot = BigDot()

game_start = time.time()
ghosts_released = 0
release_time = 5  # seconds

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == ord('w'):
				pac_man.next_facing = 'U'
			elif event.key == ord('a'):
				pac_man.next_facing = 'L'
			elif event.key == ord('s'):
				pac_man.next_facing = 'D'
			elif event.key == ord('d'):
				pac_man.next_facing = 'R'

	display.blit(map_image, (0, 0))

	time_since_start = time.time() - game_start
	if enemies_names and time_since_start // release_time + 1 > ghosts_released:
		ghosts_released += 1
		enemies[enemies_names.pop()].wall = {3}

	if pac_man.can_move_towards(pac_man.next_facing, True):
		pac_man.facing = pac_man.next_facing
		pac_man.next_facing = None

	if pac_man.god_mode and pac_man.god_mode_till < time.time():
		pac_man.god_mode = False
		pac_man.god_mode_till = None
		for enemy in enemies.values():
			if enemy.scared and not enemy.dead:
				enemy.scared = False
				enemy.set_images('alive')

	if not pac_man.dead:
		pac_man.move()
	pac_man.draw(display)

	for enemy in enemies.values():
		if not pac_man.dead:
			enemy.move_or_turn()
		enemy.draw(display)
		if pac_man.does_collide(enemy) and not pac_man.dead:
			if not enemy.scared and not enemy.dead:
				pac_man.dead = True
				pac_man.set_images('death')
				pac_man.frames_per_image = 12
			elif not enemy.dead:
				enemy.dead = True
				enemy.set_images('eyes')
				enemy.speed = 8
				enemy.rect[0] -= (enemy.rect[0] + 4) % TILE_WIDTH
				enemy.rect[1] -= (enemy.rect[1] + 4) % TILE_HEIGHT

	dots_left = False
	for y, row in enumerate(tiles):
		for x, val in enumerate(row):
			if val == 1:
				dots_left = True
				cord = x * TILE_WIDTH + 20, y * TILE_HEIGHT + 20
				small_dot.draw(display, cord)
				if pac_man.does_collide(small_dot):
					tiles[y][x] = 0
			if val == 2:
				dots_left = True
				cord = x * TILE_WIDTH + 15, y * TILE_HEIGHT + 20
				big_dot.draw(display, cord)
				if pac_man.does_collide(big_dot):
					tiles[y][x] = 0
					pac_man.god_mode = True
					pac_man.god_mode_till = time.time() + 5
					for enemy in enemies.values():
						if not enemy.dead:
							enemy.scared = True
							enemy.set_images('scared')

	if dots_left and (not pac_man.dead or not pac_man.rendered_first_cycle):
		pygame.display.update()
		clock.tick(FPS)

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

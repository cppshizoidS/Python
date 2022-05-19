import pygame
from os import path

class ImageDrawer:
    def __init__(self, player):
        pass

    def load_image(self, song_name):
        if not path.isfile('./images' + song_name + '.jpg'):


        image = pygame.image.load('./images' + song_name + '.jpg')
        return image

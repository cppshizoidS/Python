import pygame
import params


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PHERO = (255, 70, 0)
RED = (255, 0, 0)
WALL = (50, 70, 15)
WHITE = (255, 255, 255)

colors = {"FOOD":GREEN, "WALL" : WALL, "NEST" : BLUE, "ROAD" : WHITE}

class Cell(object):
    """ Defining the Cell object
    """
    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.count = 0
        self.phero = params.phero_min
        self.phero_min = params.phero_min
        self.phero_max = params.phero_max
        self.evaporate = params.evaporate

        self.type = "ROAD"
        self.color = WHITE
        self.intensity = 0

    # refresh the cell stats :
    #            evaporate the pheromone
    #            the food cells are set to pharo_max"""
    def update(self):
        """ Update the cell by evaporating the pheromone traces and
            update the intensity variable
            Intensity reflects the alpha of the pheromone color

        """
        if self.type == "FOOD":
            self.phero = self.phero_max
        elif self.type == "ROAD":
            self.phero = min(max(self.phero*self.evaporate, self.phero_min), self.phero_max)
            self.intensity = 255*(self.phero-self.phero_min)/(self.phero_max-self.phero_min)

    def draw(self, display, block_size):
        """ Draw the cell on the PyGame display
            Black if contains ant
            Blue for Nest
            Green for food
            Orange for pheromone

        """
        if self.count > 0:
            self.color = BLACK
        else:
            self.color = colors[self.type]

        pygame.draw.rect(display, self.color,\
                         [self.x*block_size, self.y*block_size, block_size, block_size])

        if self.type == "ROAD":
            temp_surf = pygame.Surface((block_size, block_size), pygame.SRCALPHA)
            temp_surf.fill((PHERO[0], PHERO[1], PHERO[2], self.intensity))
            display.blit(temp_surf, (self.x*block_size, self.y*block_size))

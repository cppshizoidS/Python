# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 17:51:50 2017

@author: Ayoub


Defining the Ant class
"""
###############################################################################
import random
import bisect
import numpy as np
import params


directions_vect = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
directions = {i:directions_vect[i] for i in range(8)}


class Ant(object):
    """ Ant Class
    """
    def __init__(self, grid):
        """ Initializing the ants
        """

        self.grid = grid
        self.x, self.y = random.choice(self.grid.nests)

        self.alpha = params.alpha
        self.beta = params.beta

        self.phero_min = params.phero_min
        self.phero_max = params.phero_max

        self.has_food = False
        self.distance = 500

        self.weights = np.zeros(8)
        self.direction = random.randint(0, 7)

    def reset(self):
        """ The ant restarts from a random nest
        """
        self.has_food = False
        self.distance = 500

        self.weights = np.zeros(8)
        self.direction = random.randint(0, 7)

        self.x, self.y = random.choice(self.grid.nests)

    def when_has_food(self):
        """ Returns the pheromone quantity to scatter if the ant carries food
        """
        return self.phero_max

    def when_no_food(self):
        """ Returns the pheromone quantity to scatter when ant doesn't has food
        """
        return (self.phero_max-self.phero_min)/50

    def scatter_phero(self):
        """ Add the pheromone to the current cell
        """


        if self.has_food:
            self.grid[self.x, self.y].phero = self.when_has_food()
        else:
            self.grid[self.x, self.y].phero += self.when_no_food()


    def weights_vector(self):
        """ Update the vector self.weights of the weightes of the directions
        """
        for i in range(8):
            self.weights[i] = 0
            if i != (self.direction+4)%8:
                dest = np.array(directions[i])+[self.x, self.y]

                try:
                    if self.grid[dest].type != "WALL":
                        if self.direction%2:
                            self.weights[i] = \
                            self.grid[dest].phero**self.alpha\
                            *np.sqrt(2)**self.beta
                        else:
                            self.weights[i] = self.grid[dest].phero**self.alpha

                except:
                    self.weights[i] = 0
                    print("Error accessing cell", dest, "in the grid")
        self.weights /= 1+np.abs(np.arange(8)-self.direction)


    def choose_direction(self):
        """ Updates the self.direction based on radom choice of weighted directions
            Weights using the weights self.weights
        """
        self.weights_vector()
        total = sum(self.weights)
        if total != 0:

            self.direction = bisect.bisect(np.cumsum(self.weights)/total, random.random())
            return True
        return False

    def rotate(self):
        """ Performs a 45° rotation clockwise
        """
        self.direction = (self.direction+1)%8


    def work(self): # the brain
        """ The algorithm of the ant movment
        """
        # Scatter pheromone in the current cell
        self.scatter_phero()

        # If a direction has been chosen
        if self.choose_direction():

            # decrement the ants count in the current cell
            self.grid[self.x, self.y].count -= 1

            # destination is the direction in vector form
            destination = directions[self.direction]

            # Move to next cell
            self.x += destination[0]
            self.y += destination[1]

            # Increment ants count in new cell
            self.grid[self.x, self.y].count += 1

            #decrmetn distance runned
            self.distance -= 1

        # If no direction has been returned : blocked path
        else:
            # Do a 180° turn
            self.direction = (self.direction+4)%8

        # If new cell has food :
        #       mark ant as has food and intialize distance
        #       do a 180° turn
        if self.grid[self.x, self.y].type == "FOOD":
            self.has_food = True
            self.distance = 500
            self.direction = (self.direction+4)%8

        # If the new cell is the nest : reset ant and decrement ants count
        if self.grid[self.x, self.y].type == "NEST" or self.distance<0:
            self.grid[self.x, self.y].count -= 1
            self.reset()

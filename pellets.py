import pygame
from abc import ABC, abstractmethod
import numpy as np
from vector import Vector2
from constants import *

# Define an abstract base class to represent pellets
class Pellet(ABC):
    # Initialize pellet properties
    def __init__(self, row, column):
        self.position = Vector2(column*TILEWIDTH, row*TILEHEIGHT)
        self.visible = True

    # Render the pellet on screen (must be implemented in concrete subclasses)
    @abstractmethod
    def render(self, screen):
        pass
        
# Define a concrete subclass to represent regular pellets
class RegularPellet(Pellet):
    # Initialize regular pellet properties
    def __init__(self, row, column):
        super().__init__(row, column)
        self.name = PELLET
        self.color = WHITE
        self.radius = int(2 * TILEWIDTH / 16)
        self.collideRadius = 2 * TILEWIDTH / 16
        self.points = 10

    # Render the regular pellet on screen
    def render(self, screen):
        if self.visible:
            # Center the pellet in its tile
            adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
            p = self.position + adjust
            pygame.draw.circle(screen, self.color, p.asInt(), self.radius)

# Define a concrete subclass to represent power pellets (inherits from Pellet class)
class PowerPellet(RegularPellet):
    # Initialize power pellet properties
    def __init__(self, row, column):
        super().__init__(row, column)
        self.name = POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flashTime = 0.2
        self.timer= 0

        # Set the color based on the pellet's position
        if (row + column) % 5 == 0:
            self.color = BLUE
        elif (row + column) % 5 == 1:
            self.color = RED
        elif (row + column) % 5 == 2:
            self.color = GREEN
        elif (row + column) % 5 == 3:
            self.color = ORANGE
        else:
            self.color = PURPLE
    # Update power pellet status and visibility
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0

    # Render the power pellet on screen
    def render(self, screen):
        if self.visible:
            # Center the pellet in its tile
            adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
            p = self.position + adjust
            # Draw a circle of given color and radius at the desired position
            pygame.draw.circle(screen, self.color, p.asInt(), self.radius)


# Define a class to represent a collection of pellets
class PelletGroup(object):
    # Initialize an empty list of pellets and power pellets
    def __init__(self, pelletfile):
        self.pelletList = []
        self.powerpellets = []
        # Create the list of pellets based on data from a file
        self.createPelletList(pelletfile)
        self.numEaten = 0

    # Update the status and visibility of all power pellets
    def update(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)

    # Create a new list of pellets based on data from a file
    def createPelletList(self, pelletfile):
        data = self.readPelletfile(pelletfile)        
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']:
                    # Create a new regular pellet
                    self.pelletList.append(RegularPellet(row, col))
                elif data[row][col] in ['P', 'p']:
                    # Create a new power pellet and add it to both lists
                    pp = PowerPellet(row, col)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)

    # Read in a data file containing information about the pellets
    def readPelletfile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
    
    # Determine whether there are no more pellets left
    def isEmpty(self):
        if len(self.pelletList) == 0:
            return True
        return False
    
    # Render all pellets on the screen
    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)
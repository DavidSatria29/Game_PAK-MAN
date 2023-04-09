from abc import ABC, abstractmethod

# Import necessary libraries and modules
import pygame
from constants import *
import numpy as np
from animation import Animator
import random

# Define some constant values
BASETILEWIDTH = 16
BASETILEHEIGHT = 16
DEATH = 5

class Sprite(ABC):
    @abstractmethod
    def getImage(self, x, y, width, height):
        pass
        
class Spritesheet(Sprite):
    def __init__(self):
        # Load the sprite sheet image and set its transparent color key
        self.__sheet = pygame.image.load("spritesheet_mspacman.png").convert()
        transcolor = self.__sheet.get_at((0,0))
        self.__sheet.set_colorkey(transcolor)
        # Scale the sprite sheet image to fit the size of the game screen
        width = int(self.__sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.__sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.__sheet = pygame.transform.scale(self.__sheet, (width, height))


    def getSheet(self):
        return self.__sheet
    # Extract an image from the sprite sheet based on its position and size
    def getImage(self, x, y, width, height):
        # Convert tile coordinates to pixel coordinates
        x *= TILEWIDTH
        y *= TILEHEIGHT
        # Set a clip area within the sprite sheet corresponding to the desired image
        self.__sheet.set_clip(pygame.Rect(x, y, width, height))
        # Return a subsurface of the sprite sheet containing only the desired image
        return self.__sheet.subsurface(self.__sheet.get_clip())


class PacmanSprites(Spritesheet):
    def __init__(self, entity):
        # Call the parent constructor to load the sprite sheet image
        Spritesheet.__init__(self)
        # Store a reference to the entity object that this sprite represents
        self.entity = entity
        # Set the initial image of the entity object to the starting image for Pacman
        self.entity.image = self.getStartImage()
        # Define dictionaries to store animation data and the default "stop" image
        self.animations = {}
        self.defineAnimations()
        self.stopimage = (8, 0)

    # Define the various animations for Pacman's movement and death
    def defineAnimations(self):
        self.animations[LEFT] = Animator(((8,0), (0, 0), (0, 2), (0, 0)))
        self.animations[RIGHT] = Animator(((10,0), (2, 0), (2, 2), (2, 0)))
        self.animations[UP] = Animator(((10,2), (6, 0), (6, 2), (6, 0)))
        self.animations[DOWN] = Animator(((8,2), (4, 0), (4, 2), (4, 0)))
        self.animations[DEATH] = Animator(((0, 12), (2, 12), (4, 12), (6, 12), (8, 12), (10, 12), (12, 12), (14, 12), (16, 12), (18, 12), (20, 12)), speed=6, loop=False)

    # Update the entity object's image based on its current state and direction
    def update(self, dt):
        # If the entity is still alive, update its image based on its current direction
        if self.entity.alive == True:
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(*self.animations[LEFT].update(dt))
                self.stopimage = (8, 0)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(*self.animations[RIGHT].update(dt))
                self.stopimage = (10, 0)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(*self.animations[DOWN].update(dt))
                self.stopimage = (8, 2)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(*self.animations[UP].update(dt))
                self.stopimage = (10, 2)
            elif self.entity.direction == STOP:
                self.entity.image = self.getImage(*self.stopimage)
        # If the entity has died, update its image to show the death animation
        else:
            self.entity.image = self.getImage(*self.animations[DEATH].update(dt))


    # Define a method to reset all animations to their start position
    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()

    # Define a method to get the starting image for Pacman
    def getStartImage(self):
        return self.getImage(8, 0)

    # Define a method to get an image from the sprite sheet given its position
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)



# Define a GhostSprites class that inherits from the Spritesheet class
class GhostSprites(Spritesheet):
    def __init__(self, entity):
        # Call the parent constructor to load the sprite sheet image
        Spritesheet.__init__(self)
        # Set the initial x coordinates for each ghost type
        self.x = {BLINKY:0, PINKY:2, INKY:4, CLYDE:6}
        # Store a reference to the entity object that this sprite represents
        self.entity = entity
        # Set the entity's initial image to the starting image for this ghost type
        self.entity.image = self.getStartImage()

    # Update the entity object's image based on its current state and direction
    def update(self, dt):
        # Get the appropriate x coordinate for this ghost type
        x = self.x[self.entity.name]
        if self.entity.mode.current in [SCATTER, CHASE]:
            # If the ghost is in scatter or chase mode, update its image based on its direction of movement
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(x, 8)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(x, 10)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(x, 6)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(x, 4)
        elif self.entity.mode.current == FREIGHT:
            # If the ghost is in fright mode, update its image to show the frightened state
            self.entity.image = self.getImage(10, 4)
        elif self.entity.mode.current == SPAWN:
            # If the ghost is in spawn mode, update its image based on its direction of movement
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(8, 8)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(8, 10)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(8, 6)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(8, 4)

    # Define a method to get the starting image for this ghost type
    def getStartImage(self):
        return self.getImage(self.x[self.entity.name], 4)

    # Define a method to get an image from the sprite sheet given its position, accounting for tile width and height
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

# Define a FruitSprites class that inherits from the Spritesheet class
class FruitSprites(Spritesheet):
    def __init__(self, entity, level):
        # Call the parent constructor to load the sprite sheet image
        Spritesheet.__init__(self)
        # Store a reference to the entity object that this sprite represents
        self.entity = entity
        # Set up a dictionary of fruit sprites and their positions in the sprite sheet
        self.fruits = {0:(16,8), 1:(18,8), 2:(20,8), 3:(16,10), 4:(18,10), 5:(20,10)}
        # Set the entity's initial image to the starting image for the current level and fruit type
        self.entity.image = self.getStartImage(level % len(self.fruits))

    # Define a method to get the starting image for this fruit type
    def getStartImage(self, key):
        return self.getImage(*self.fruits[key])

    # Define a method to get an image from the sprite sheet given its position, accounting for tile width and height
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


# Define a LifeSprites class that inherits from the Spritesheet class
class LifeSprites(Spritesheet):
    def __init__(self, numlives):
        # Call the parent constructor to load the sprite sheet image
        Spritesheet.__init__(self)
        # Call the resetLives() method to create images for each life represented by the given number
        self.resetLives(numlives)

    # Remove the first image from the list of life images
    def removeImage(self):
        if len(self.images) > 0:
            self.images.pop(0)

    # Reset the life images to represent the given number of lives
    def resetLives(self, numlives):
        self.images = []
        for i in range(numlives):
            self.images.append(self.getImage(0,0))

    # Define a method to get an image from the sprite sheet given its position, accounting for tile width and height
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


# Define a MazeSprites class that inherits from the Spritesheet class
class MazeSprites(Spritesheet):
    def __init__(self, mazefile, rotfile):
        # Call the parent constructor to load the sprite sheet image
        Spritesheet.__init__(self)
        # Load the maze data from a file and store it as an instance variable
        self.data = self.readMazeFile(mazefile)
        # Load the rotation data from a file and store it as an instance variable
        self.rotdata = self.readMazeFile(rotfile)

    # Define a method to get an image for a given position on the sprite sheet, accounting for tile width and height
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, TILEWIDTH, TILEHEIGHT)

    # Define a method to read a maze file into a numpy array
    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    # Define a method to construct the maze background given a blank surface and a vertical position value
    def constructBackground(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    # Get the index of the sprite representing the current maze cell
                    x = int(self.data[row][col]) + 12
                    # Get the corresponding sprite image from the sprite sheet and rotate it based on rotation data
                    sprite = self.getImage(x, y)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    # Draw the sprite onto the background surface at the correct location
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))
                elif self.data[row][col] == '=':
                    # Draw an obstacle sprite onto the background surface at the correct location
                    sprite = self.getImage(10, 8)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))
        return background

    # Define a method to rotate a sprite image by a given number of 90-degree increments
    def rotate(self, sprite, value):
        return pygame.transform.rotate(sprite, value*90)


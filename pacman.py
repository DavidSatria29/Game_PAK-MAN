import pygame  # import the pygame library for game development
from pygame.locals import *  # import the pygame constants for easy access
from vector import Vector2  # import a custom Vector2 class for 2D vector operations
from constants import *  # import custom constants for the game
from entity import Entity  # import a custom Entity class for game entities
from sprites import PacmanSprites  # import custom sprite classes for Pacman

class Pacman(Entity):  # define a custom Pacman class that inherits from Entity
    def __init__(self, node):  # initialize a Pacman object with a starting node
        Entity.__init__(self, node )  # call the __init__ method of the parent class to initialize basic attributes
        self.name = PACMAN  # set the name of the Pacman object to "PACMAN"
        self.color = YELLOW  # set the color of the Pacman object to YELLOW
        self.direction = LEFT  # set the initial direction of Pacman to LEFT
        self.setBetweenNodes(LEFT)  # set Pacman's position between two nodes
        self.alive = True  # set Pacman's initial state to alive
        self.sprites = PacmanSprites(self)  # create an instance of the PacmanSprites class for the Pacman object

    def reset(self):  # define a reset method to reset Pacman's attributes to their initial values
        Entity.reset(self)  # call the reset method of the parent class to reset basic attributes
        self.direction = LEFT  # set Pacman's direction to LEFT
        self.setBetweenNodes(LEFT)  # set Pacman's position between two nodes
        self.alive = True  # set Pacman's state to alive
        self.image = self.sprites.getStartImage()  # set the image of Pacman to its start image
        self.sprites.reset()  # reset the PacmanSprites object

    def die(self):  # define a die method to set Pacman's state to dead
        self.alive = False  # set Pacman's state to dead
        self.direction = STOP  # set Pacman's direction to STOP

    def update(self, dt):
        # Update the sprites
        self.sprites.update(dt)
        # Update the position based on direction and speed
        self.position += self.directions[self.direction] * self.speed * dt
        # Get the next valid direction from user input
        direction = self.getValidKey()
        # Check if the target position has been reached
        if self.overshotTarget():
            # Set the current node as the target node
            self.node = self.target
            # If the current node has a portal, set the target node as the portal's neighbor
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            # Get the next target node based on the new direction
            self.target = self.getNewTarget(direction)
            # If the target is not the current node, update the direction
            if self.target is not self.node:
                self.direction = direction
            else:
                # If the target is the current node, keep moving in the current direction
                self.target = self.getNewTarget(self.direction)
            # If the target is the current node, stop moving
            if self.target is self.node:
                self.direction = STOP
            # Update the position
            self.setPosition()
        else:
            # If the target position has not been reached, check if the new direction is opposite to the current direction
            if self.oppositeDirection(direction):
                # If the new direction is opposite, reverse the direction
                self.reverseDirection()

    def getValidKey(self):
        # Get the currently pressed key from the user
        key_pressed = pygame.key.get_pressed()
        # If the up key is pressed, return the UP direction
        if key_pressed[K_UP]:
            return UP
        # If the down key is pressed, return the DOWN direction
        if key_pressed[K_DOWN]:
            return DOWN
        # If the left key is pressed, return the LEFT direction
        if key_pressed[K_LEFT]:
            return LEFT
        # If the right key is pressed, return the RIGHT direction
        if key_pressed[K_RIGHT]:
            return RIGHT
        # If no key is pressed, return the STOP direction
        return STOP

    def eatPellets(self, pelletList):
        # Check if the player collides with any pellet from the list
        for pellet in pelletList:
            if self.collideCheck(pellet):
                # If there is a collision, return the collided pellet
                return pellet
        # If there is no collision, return None
        return None

    def collideGhost(self, ghost):
        # Check if the player collides with the ghost
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        # Check if there is a collision between the player and the other object
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius) ** 2
        if dSquared <= rSquared:
            # If there is a collision, return True
            return True
        # If there is no collision, return False
        return False
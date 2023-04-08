import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint
from abc import ABC, abstractmethod

class BaseEntity(ABC):
    def __init__(self, node):
        # initialize the BaseEntity object
        self.name = None
        self.directions = {UP:Vector2(0, -1),DOWN:Vector2(0, 1), 
                          LEFT:Vector2(-1, 0), RIGHT:Vector2(1, 0), STOP:Vector2()}
        # define a dictionary for different directions with Vector2 values
        self.direction = STOP # initially set direction to STOP
        self.setSpeed(100) # set the speed of the entity
        self.radius = 10 # set the radius of the entity
        self.collideRadius = 5 # set the collision radius of the entity
        self.color = WHITE # set the color of the entity
        self.visible = True # set the visibility of the entity to true
        self.disablePortal = False # set disablePortal flag to False
        self.goal = None # initially set the goal to none
        self.directionMethod = self.randomDirection # set direction method to random direction
        self.setStartNode(node) # set the starting node of the entity
        self.image = None # set the image of the entity to None
        
    @abstractmethod
    def update(self, dt):
        pass
    
    @abstractmethod
    def render(self, screen):
        pass

    def setPosition(self):
        self.position = self.node.position.copy() # set the position of the entity to its current node's position

    def validDirection(self, direction):
        # check if the given direction is a valid direction for the entity to move 
        # based on the current node and the access available in that direction
        if direction is not STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False

    def getNewTarget(self, direction):
        # get the new target node based on the given direction
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshotTarget(self):
        # this method returns True if the entity has passed its target node and False otherwise
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False

    def reverseDirection(self):
        # reverse the direction of the entity and exchange the current and target nodes
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp
        
    def oppositeDirection(self, direction):
        # return True if the given direction is opposite to the current direction of the entity
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def validDirections(self):
        # this method returns a list of all the valid directions that an entity can move in
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.validDirection(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1) #if no valid directions are available, move back in the opposite direction
        return directions

    def randomDirection(self, directions):
        # this method returns a random direction from the given list of directions
        return directions[randint(0, len(directions)-1)]

    def goalDirection(self, directions):
        # this method returns the direction which takes the entity closer to its goal position
        distances = []
        for direction in directions:
            vec = self.node.position  + self.directions[direction]*TILEWIDTH - self.goal
            distances.append(vec.magnitudeSquared()) #calculate squared magnitude of vectors
        index = distances.index(min(distances)) #get the index of the minimum distance
        return directions[index]

    def setStartNode(self, node):
        # set the starting node of the entity
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()

    def setBetweenNodes(self, direction):
        # set the target node between the current node and its neighbor in the given direction
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    def reset(self):
        # reset the entity's attributes to its starting state
        self.setStartNode(self.startNode)
        self.direction = STOP
        self.speed = 100
        self.visible = True

    def setSpeed(self, speed):
        # set the speed of the entity in pixels per second
        self.speed = speed * TILEWIDTH / 16

class Entity(BaseEntity):
    def __init__(self, node):
        super().__init__(node)
    
    def update(self, dt):
        # update the position of the entity based on its direction and speed
        self.position += self.directions[self.direction]*self.speed*dt
        if self.overshotTarget():
            # if the entity overshot its target, reset the node, get new directions and set the position
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction # set the direction towards the new target
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition() # set the position of the entity
            
    def render(self, screen):
        # render the entity on the given screen
        if self.visible:
            if self.image is not None:
                adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
                p = self.position - adjust
                screen.blit(self.image, p.asTuple())
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)

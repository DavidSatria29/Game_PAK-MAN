import pygame
from entity import Entity    #importing Entity class from entity.py file
from constants import *      #importing all constant variables from constants.py file
from sprites import FruitSprites   #importing FruitSprites class from sprites.py file

class Fruit(Entity):
    def __init__(self, node, level=0):
        #constructor method of the Fruit class
        super().__init__(node)#calling constructor of the super (Entity) class
        self.name = FRUIT    #setting the name of the Fruit object
        self.color = GREEN   #setting the color of the Fruit object
        self.lifespan = 5    #setting the lifespan of the Fruit object
        self.timer = 0       #setting the timer of the Fruit object
        self.destroy = False #setting the destroy flag to false for the Fruit object
        self.points = 100 + level*20 #calculating points based on the level of the game
        self.setBetweenNodes(RIGHT)  #setting the target node in the right direction
        self.sprites = FruitSprites(self, level) #creating a new FruitSprites object for the Fruit object

    def update(self, dt):
        #update method to update the Fruit object's timer and check if it needs to be destroyed
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True

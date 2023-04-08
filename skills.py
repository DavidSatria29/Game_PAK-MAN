import pygame
from entity import Entity    #importing Entity class from entity.py file
from constants import *      #importing all constant variables from constants.py file
from sprites import SkillsSpirites   #importing FruitSprites class from sprites.py file
from pacman import Pacman


class Skill(Entity):
    def __init__(self, node:int, name):
        #constructor method of the Fruit class
        super().__init__(node)#calling constructor of the super (Entity) class
        self.name = name    #setting the name of the Fruit object
        self.color = YELLOW   #setting the color of the Fruit object
        self.lifespan = 6    #setting the lifespan of the Fruit object
        self.timer = 0       #setting the timer of the Fruit object
        self.destroy = False #setting the destroy flag to false for the Skill object
        self.setBetweenNodes(RIGHT)  #setting the target node in the right direction
        self.spirites = SkillsSpirites(self) #Creating a new Skills Spirit object for the Skill Object
        self.pacman = Pacman(self)

    def update(self, dt):
        #update method to update the Fruit object's timer and check if it needs to be destroyed
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True
    

class Speed_Increase(Skill):
    def __init__(self, node:int, name):
        super().__init__(node, name)
        self.name:str = SPEED_INCREASE

    def newUpdate(self):
        if(self.update()):
            self.pacman.setSpeed(20)


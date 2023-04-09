# Import required modules and constants for the Text class
import pygame
from vector import Vector2
from constants import *

# Define a Text class to represent a text label on screen
class Text(object):
    # Initialize instance variables for the unique ID, text content, color, size, visibility, position, timer, lifespan, label, and destroy flag
    def __init__(self, text, color, x, y, size, time=None, id=None, visible=True):
        self.id = id
        self.text = text
        self.color = color
        self.size = size
        self.visible = visible
        self.position = Vector2(x, y)
        self.timer = 0
        self.lifespan = time
        self.label = None
        self.destroy = False
        # Call helper methods to set up font and create label surface
        self.setupFont("PressStart2P-Regular.ttf")
        self.createLabel()

    # Set up the font typeface and size for the text label
    def setupFont(self, fontname):
        self.font = pygame.font.Font(fontname, self.size)

    # Create the text label as a rendered surface
    def createLabel(self):
        self.label = self.font.render(self.text, True, self.color)

    # Update the text label based on the current delta time value
    def update(self, dt):
        # If a lifespan has been specified, update the timer and flag for destruction when expired
        if self.lifespan is not None:
            self.timer += dt
            if self.timer > self.lifespan:
                self.destroy = True

    # Set the text content of the label to the specified value
    def setText(self, text):
        self.text = text
        self.createLabel()

    # Render the text label on the specified screen surface
    def render(self, screen):
        if self.visible:
            screen.blit(self.label, self.position.get())

    # Get the width and height of the rendered label surface
    def getSize(self):
        return self.label.get_size()
    
    # Set up the font typeface and size for the text label
    def setupFont(self, fontpath):
        self.font = pygame.font.Font(fontpath, self.size)

    # Create the text label as a rendered surface
    def createLabel(self):
        self.label = self.font.render(self.text, 1, self.color)

    # Update the text content of the label to the specified value
    def setText(self, newtext):
        self.text = str(newtext)
        self.createLabel()

    # Update the text label based on the current delta time value
    def update(self, dt):
        # If a lifespan has been specified, update the timer and flag for destruction when expired
        if self.lifespan is not None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0
                self.lifespan = None
                self.destroy = True

    # Render the text label on the specified screen surface
    def render(self, screen):
        # If visible, convert position Vector2 to tuple and blit the label on the screen
        if self.visible:
            x, y = self.position.asTuple()
            screen.blit(self.label, (x, y))

class TextGroup(object):
    def __init__(self):
        # Initialize instance variables for the next unique ID, all text labels, and setup initial text labels
        self.nextid = 10
        self.alltext = {}
        self.setupText()
        # Show the initial "READY!" text label
        self.showText(READYTXT)

    # Add a new text label to the group with the specified properties and return its unique ID
    def addText(self, text, color, x, y, size, time=None, id=None):
        self.nextid += 1
        self.alltext[self.nextid] = Text(text, color, x, y, size, time=time, id=id)
        return self.nextid

    # Remove a text label from the group by its unique ID
    def removeText(self, id):
        self.alltext.pop(id)
        
    # Set up the initial text labels for score, level, and game status
    def setupText(self):
        size = TILEHEIGHT
        self.alltext[SCORETXT] = Text("0".zfill(8), WHITE, 0, TILEHEIGHT, size)
        self.alltext[HIGHESTSCORE] = Text("0".zfill(8), WHITE, 10*TILEWIDTH, TILEHEIGHT, size)
        self.alltext[LEVELTXT] = Text(str(1).zfill(3), WHITE, 23*TILEWIDTH, TILEHEIGHT, size)
        self.alltext[READYTXT] = Text("READY!", YELLOW, 11.25*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.alltext[PAUSETXT] = Text("PAUSED!", YELLOW, 10.625*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.alltext[GAMEOVERTXT] = Text("GAMEOVER!", YELLOW, 10*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.addText("SCORE", WHITE, 0, 0, size)
        self.addText("HIGHEST SCORE", WHITE, 10*TILEWIDTH, 0, 2 * size //3)
        self.addText("LEVEL", WHITE, 23*TILEWIDTH, 0, size)

    # Update all text labels in the group based on the specified delta time value
    def update(self, dt):
        for tkey in list(self.alltext.keys()):
            # Update the individual text label and remove if flagged for destruction
            self.alltext[tkey].update(dt)
            if self.alltext[tkey].destroy:
                self.removeText(tkey)

    # Show a specific text label in the group by its unique ID and hide all others
    def showText(self, id):
        self.hideText()
        self.alltext[id].visible = True

    # Hide all game status-related text labels (READY!, PAUSED!, GAMEOVER!)
    def hideText(self):
        self.alltext[READYTXT].visible = False
        self.alltext[PAUSETXT].visible = False
        self.alltext[GAMEOVERTXT].visible = False

    # Update the score text label with the current score value
    def updateScore(self, score):
        self.updateText(SCORETXT, str(score).zfill(8))

    # Update the highest score text label if the current score is greater than the existing highest score
    def updateHighScore(self, score):
        self.updateText(HIGHESTSCORE, str(score).zfill(8))

    # Update the level text label with the current level value
    def updateLevel(self, level):
        self.updateText(LEVELTXT, str(level + 1).zfill(3))

    # Update a specific text label with a new value by its unique ID
    def updateText(self, id, value):
        if id in self.alltext.keys():
            self.alltext[id].setText(value)

    # Render all text labels in the group on the specified screen surface
    def render(self, screen):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].render(screen)


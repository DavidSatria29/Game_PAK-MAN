# Import required modules and classes 
import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pauser import Pause
from text import TextGroup
from sprites import LifeSprites
from sprites import MazeSprites
from mazedata import MazeData

#musik
pygame.mixer.init()
suara_jalan = pygame.mixer.Sound('jalan.mp3')
suara_mati = pygame.mixer.Sound('mati.wav')
suara_menang = pygame.mixer.Sound('menang.wav')
suara_makan = pygame.mixer.Sound('pelet.wav')
suara_bunuh = pygame.mixer.Sound('bunuh.wav')
suara_medkit = pygame.mixer.Sound('medkit.wav')
suara_slowmo = pygame.mixer.Sound('slowmo.wav')
suara_speed = pygame.mixer.Sound('speed.wav')
suara_hantu = pygame.mixer.Sound('hantu.wav')
suara_teleport = pygame.mixer.Sound('teleport.wav')
pygame.mixer.music.load('musik2.mp3')
pygame.mixer.music.play(-1)

# Define GameController class
class GameController(object):
    # Initialize GameController object
    def __init__(self):
        # Initialize pygame library
        pygame.init()
        # Set game screen resolution and create a display surface
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.title = pygame.display.set_caption("PAK-MAN")
        self.background = None
        self.background_norm = None
        self.background_flash = None
        # Create a clock object to measure time in the game
        self.clock = pygame.time.Clock()
        # Initialize objects related to game elements
        self.fruit = None
        self.skills = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.fruitCaptured = []
        self.fruitNode = None
        self.mazedata = MazeData()


    # Define method to set game background
    def setBackground(self):
        # Create two surface objects for the normal and flashing background
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        # Construct the maze background using the MazeSprites class
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, self.level%5)
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)
        # Set initial values for flashing background flag and active background
        self.flashBG = False
        self.background = self.background_norm

    # Define method to start the game 
    def startGame(self):  
        # Load maze data for the current level
        self.mazedata.loadMaze(self.level)
        # Initialize MazeSprites object to handle maze element rendering
        self.mazesprites = MazeSprites(self.mazedata.obj.name+".txt", self.mazedata.obj.name+"_rotation.txt")
        # Set the game background using MazeSprites and NodeGroup classes
        self.setBackground()
        self.nodes = NodeGroup(self.mazedata.obj.name+".txt")
        self.mazedata.obj.setPortalPairs(self.nodes)
        self.mazedata.obj.connectHomeNodes(self.nodes)
        # Initialize Pacman, PelletGroup, and GhostGroup objects
        self.pacman = Pacman(self.nodes.getNodeFromTiles(*self.mazedata.obj.pacmanStart))
        self.pellets = PelletGroup(self.mazedata.obj.name+".txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
        # Set starting nodes and access restrictions for each ghost
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(0, 3)))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(4, 3)))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 0)))
        # Set access restrictions for Pacman and ghosts in certain areas of the maze
        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.mazedata.obj.denyGhostsAccess(self.ghosts, self.nodes)

    # Define outdated method to start the game 
    def startGame_old(self):      
        # Load maze data for the current level
        self.mazedata.loadMaze(self.level)#(This line loads the maze data for the selected game level)
        # Initialize MazeSprites object to handle maze element rendering
        self.mazesprites = MazeSprites("maze1.txt", "maze1_rotation.txt")
        # Set the game background using MazeSprites and NodeGroup classes
        self.setBackground()
        self.nodes = NodeGroup("maze1.txt")
        # Set portal pair and create home key
        self.nodes.setPortalPair((0,17), (27,17))
        homekey = self.nodes.createHomeNodes(11.5, 14)
        # Connect home nodes and initialize Pacman, PelletGroup, and GhostGroup objects
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))
        self.pellets = PelletGroup("maze1.txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
        # Set starting nodes for each ghost
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 0+14))
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(0+11.5, 3+14))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(4+11.5, 3+14))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        # Set access restrictions for Pacman and ghosts in certain areas of the maze
        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.nodes.denyAccessList(12, 14, UP, self.ghosts)
        self.nodes.denyAccessList(15, 14, UP, self.ghosts)
        self.nodes.denyAccessList(12, 26, UP, self.ghosts)
        self.nodes.denyAccessList(15, 26, UP, self.ghosts)

    # Define update method to handle updating various game events based on elapsed time
    def update(self):
        # Set time delta using Pygame clock and convert to seconds
        dt = self.clock.tick(30) / 1000.0
        # Update text group and pellet group
        self.textgroup.update(dt)
        self.pellets.update(dt)
        # Check if game is paused and update ghosts, fruits, and various game events accordingly
        if not self.pause.paused:
            self.ghosts.update(dt)      
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()

        # Update Pacman if he is alive and game is not paused; otherwise just update Pacman
        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)

        # Handle flashing background based on elapsed time
        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        # Update pause method and execute after-pause method if applicable
        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        
        # Check game events and render graphics
        self.checkEvents()
        self.render()

    # Define checkEvents method to handle various events during gameplay
    def checkEvents(self):
        # Check all events in Pygame event queue
        for event in pygame.event.get():
            # Quit game if QUIT event is detected
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                # Handle pause event when spacebar is pressed
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        pygame.mixer.music.pause()
                        suara_jalan.stop()
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                            pygame.mixer.music.unpause()
                            suara_jalan.play(-1)
                        else:
                            self.textgroup.showText(PAUSETXT)

    # Define checkPelletEvents method to handle pellet-related events during gameplay
    def checkPelletEvents(self):
        # Check if Pacman eats pellets and update pellet-related game events accordingly
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                if pellet.color == ORANGE: 
                    self.ghosts.startFreight()
                    suara_makan.play()
                elif pellet.color == RED:
                    self.pacman.setSpeed(170)
                    suara_speed.play()
                elif pellet.color == BLUE:
                    self.pacman.setSpeed(70)
                    suara_slowmo.play()
                elif pellet.color == GREEN:
                    self.ghosts.reset()
                    suara_teleport.play()
                else:
                    self.ghosts.increaseSpedd()
                    suara_hantu.play()

                
            if self.pellets.isEmpty():
                self.flashBG = True
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)
                suara_menang.play()
                suara_jalan.stop()

    # Define checkGhostEvents method to handle ghost-related events during gameplay
    def checkGhostEvents(self):
        # Check collisions between Pacman and each ghost
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                # Handle events when Pacman collides with a ghost
                if ghost.mode.current is FREIGHT:  # If ghost is in "freight" mode, update game state accordingly
                    self.pacman.visible = False
                    ghost.visible = False
                    self.updateScore(ghost.points)
                    self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost)
                    suara_bunuh.play()
                elif ghost.mode.current is not SPAWN:  # If ghost is not in "spawn" mode, update game state accordingly
                    if self.pacman.alive:
                        self.lives -=  1
                        self.lifesprites.removeImage()
                        self.pacman.die()
                        self.ghosts.hide()
                        suara_jalan.stop()
                        suara_mati.play()
                        if self.lives == 1:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)
                            suara_medkit.play()
                            suara_mati.stop()
                        elif self.lives == 0 :
                            self.textgroup.showText(GAMEOVERTXT)
                            self.pause.setPause(pauseTime=3, func=self.restartGame)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)

    # Define checkFruitEvents method to handle events related to fruit in gameplay
    def checkFruitEvents(self):
        # Check if enough pellets have been eaten to spawn fruit
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            # If no fruit currently exists, create a new fruit instance
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20), self.level)
                print(self.fruit)  # Debugging statement to print the fruit object
        # If a fruit instance already exists, handle collisions and destruction accordingly
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.lives += 1
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                fruitCaptured = False
                for fruit in self.fruitCaptured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruitCaptured = True
                        break
                if not fruitCaptured:
                    self.fruitCaptured.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None


    # Define showEntities method to show entities on the screen
    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()

    # Define hideEntities method to hide entities from the screen
    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    # Define nextLevel method to transition to the next level of the game
    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)


    # Define restartGame method to reset the game to its initial state
    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()  # Call startGame method to begin a new game instance
        self.score = 0
        self.textgroup.updateScore(self.score)  # Update score text to show initial score of 0
        self.textgroup.updateLevel(self.level)  # Update level text to show initial level of 0
        self.textgroup.showText(READYTXT)  # Show "ready" text before starting the game
        self.lifesprites.resetLives(self.lives)  # Reset the number of lives sprites to the initial value of 3
        self.fruitCaptured = []  # Reset the list of captured fruit images

    # Define resetLevel method to reset the current level to its initial state
    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()  # Reset Pacman's position and animation
        self.ghosts.reset()  # Reset ghosts' positions and animations
        self.fruit = None
        self.textgroup.showText(READYTXT)  # Show "ready" text at the beginning of the level

    # Define updateScore method to update the player's score based on the points earned
    def updateScore(self, points):
        self.score += points  # Add the points earned to the player's score
        self.textgroup.updateScore(self.score)  # Update score text to show the updated score

    # Define render method to draw all game objects and update the display
    def render(self):
        self.screen.blit(self.background, (0, 0))  # Draw the background image
        self.pellets.render(self.screen)  # Draw the pellets
        if self.fruit is not None:
            self.fruit.render(self.screen)  # Draw the fruit if it exists
        self.pacman.render(self.screen)  # Draw Pacman
        self.ghosts.render(self.screen)  # Draw the ghosts
        self.textgroup.render(self.screen)  # Draw all text objects

        # Draw the life sprites in a row at the bottom of the screen
        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))

        # Draw the captured fruit images in a row at the bottom right of the screen
        for i in range(len(self.fruitCaptured)):
            x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i+1)
            y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
            self.screen.blit(self.fruitCaptured[i], (x, y))

        pygame.display.update()  # Update the display to show all changes made in this frame


# Check if this module is being run as the main program
if __name__ == "__main__":
    # Create a new instance of GameController
    game = GameController()
    # Start the game by calling startGame method
    game.startGame()
    # Loop indefinitely to update the game state and render the game
    while True:
        game.update()





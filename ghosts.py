import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController
from sprites import GhostSprites


# Ghost class inherits from Entity
class Ghost(Entity):
    def __init__(self, node: int, pacman=None, blinky=None) -> None:
        # Call Entity's constructor with the node parameter
        super().__init__(node)
        # Set some properties of the Ghost
        self.name: str = GHOST
        self.points: int = 200
        self.goal: Vector2 = Vector2()
        self.directionMethod: callable = self.goalDirection
        # Keep references to other game entities
        self.pacman = pacman
        self.mode: ModeController = ModeController(self)
        self.blinky = blinky
        self.homeNode = node

    def reset(self) -> None:
        # Call Entity's reset method and reset some Ghost properties
        super().reset()
        self.points: int = 200
        self.directionMethod: callable = self.goalDirection

    def update(self, dt: float) -> None:
        # Call Entity's update method and update Ghost's mode and sprites
        self.sprites.update(dt)
        self.mode.update(dt)
        # If in scatter mode, update goal to empty vector
        if self.mode.current is SCATTER:
            self.scatter()
        # If in chase mode, update goal to Pacman's position
        elif self.mode.current is CHASE:
            self.chase()
        # Call Entity's update method to actually update position and direction
        super().update(dt)

    def scatter(self) -> None:
        # Update Ghost's goal to an empty vector
        self.goal: Vector2 = Vector2()

    def chase(self) -> None:
        # Update Ghost's goal to Pacman's position
        self.goal: Vector2 = self.pacman.position

    def spawn(self) -> None:
        # Update Ghost's goal to its spawn node's position
        self.goal: Vector2 = self.spawnNode.position

    def setSpawnNode(self, node: int) -> None:
        # Keep a reference to Ghost's spawn node
        self.spawnNode = node

    def startSpawn(self) -> None:
        # Set Ghost's mode to Spawn and update properties accordingly
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()

    def startFreight(self) -> None:
        # Set Ghost's mode to Freight and update properties accordingly
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection

    def normalMode(self) -> None:
        # Update Ghost's speed and direction method for normal mode
        self.setSpeed(100)
        self.directionMethod = self.goalDirection
        # Deny access to the DOWN direction for Ghost's home node
        self.homeNode.denyAccess(DOWN, self)


class Blinky(Ghost):
    def __init__(self, node: int, pacman=None, blinky=None) -> None:
        super().__init__(node, pacman, blinky)
        self.name: str = BLINKY
        self.color: tuple[int, int, int] = RED
        self.sprites: GhostSprites = GhostSprites(self)

        
class Pinky(Ghost):
    def __init__(self, node: int, pacman=None, blinky=None) -> None:
        super().__init__(node, pacman, blinky)
        self.name: str = PINKY
        self.color: tuple[int, int, int] = PINK
        self.sprites: GhostSprites = GhostSprites(self)

    def scatter(self) -> None:
        # Set the scatter goal to the top-right corner of the screen
        self.goal: Vector2 = Vector2(TILEWIDTH * NCOLS, 0)

    def chase(self) -> None:
        # Set the chase goal four tiles ahead of Pacman's current position
        vec1: Vector2 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4
        self.goal: Vector2 = vec1


class Inky(Ghost):
    def __init__(self, node: int, pacman=None, blinky=None) -> None:
        super().__init__(node, pacman, blinky)
        self.name: str = INKY
        self.color: tuple[int, int, int] = TEAL
        self.sprites: GhostSprites = GhostSprites(self)

    def scatter(self) -> None:
        # Set the scatter goal to the bottom-right corner of the screen
        self.goal: Vector2 = Vector2(TILEWIDTH * NCOLS, TILEHEIGHT * NROWS)

    def chase(self) -> None:
        # Set the chase goal to a location two tiles ahead of Pacman, and twice the distance between Pacman and Blinky from Blinky
        vec1: Vector2 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        vec2: Vector2 = (vec1 - self.blinky.position) * 2
        self.goal: Vector2 = self.blinky.position + vec2



class Clyde(Ghost):
    def __init__(self, node: int, pacman=None, blinky=None) -> None:
        super().__init__(node, pacman, blinky)
        self.name: str = CLYDE
        self.color: tuple[int, int, int] = ORANGE
        self.sprites: GhostSprites = GhostSprites(self)

    def scatter(self) -> None:
        # Set the goal to the bottom left corner of the screen
        self.goal: Vector2 = Vector2(0, TILEHEIGHT * NROWS)

    def chase(self) -> None:
        # Calculate the vector from Clyde to Pacman
        d: Vector2 = self.pacman.position - self.position
        # Calculate the squared distance between Clyde and Pacman
        ds: float = d.magnitudeSquared()
        # If the distance is less than or equal to 8 tiles, scatter
        if ds <= (TILEWIDTH * 8)**2:
            self.scatter()
        # Otherwise, set the goal to 4 tiles ahead of Pacman in Pacman's current direction
        else:
            self.goal: Vector2 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

class GhostGroup(object):
    def __init__(self, node: int, pacman) -> None:
        # Create instances of each type of ghost with the specified starting node and Pacman
        self.blinky: Blinky = Blinky(node, pacman)
        self.pinky: Pinky = Pinky(node, pacman)
        self.inky: Inky = Inky(node, pacman, self.blinky)
        self.clyde: Clyde = Clyde(node, pacman)
        # Store all ghosts in a list
        self.ghosts: list[Ghost] = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self) -> iter:
        # Allow the GhostGroup instance to be iterated over
        return iter(self.ghosts)

    def update(self, dt: float) -> None:
        # Update all ghosts in the group
        for ghost in self:
            ghost.update(dt)

    def startFreight(self) -> None:
        # Start the freight mode for all ghosts in the group and reset their point values
        for ghost in self:
            ghost.startFreight()
        self.resetPoints()

    def setSpawnNode(self, node: int) -> None:
        # Set the spawn node for all ghosts in the group
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self) -> None:
        # Double the point values for all ghosts in the group
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self) -> None:
        # Reset the point values for all ghosts in the group to 200
        for ghost in self:
            ghost.points: int = 200

    def hide(self) -> None:
        # Hide all ghosts in the group
        for ghost in self:
            ghost.visible: bool = False

    def show(self) -> None:
        # Show all ghosts in the group
        for ghost in self:
            ghost.visible: bool = True

    def reset(self) -> None:
        # Reset all ghosts in the group to their default state
        for ghost in self:
            ghost.reset()

    def render(self, screen) -> None:
        # Render all ghosts in the group to the specified screen
        for ghost in self:
            ghost.render(screen)


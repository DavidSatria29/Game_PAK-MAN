# import constants module
from constants import *
# import the abc module
from abc import ABC, abstractmethod

# define the abstract base class for mazes
class MazeBase(ABC):
    def __init__(self):
        # initialize portal pairs as an empty dictionary
        self.portalPairs = {}
        # set the home offset to (0,0)
        self.homeoffset = (0, 0)
        # set the ghost node deny dictionary to empty lists for each direction
        self.ghostNodeDeny = {UP:(), DOWN:(), LEFT:(), RIGHT:()}

    # set portal pairs for the maze nodes
    @abstractmethod
    def setPortalPairs(self, nodes):
        pass

    # connect the home nodes for the maze
    @abstractmethod
    def connectHomeNodes(self, nodes):
        pass

    # add the home offset to a given coordinate
    def addOffset(self, x, y):
        return x+self.homeoffset[0], y+self.homeoffset[1]

    # deny ghost access to specific nodes in the maze
    def denyGhostsAccess(self, ghosts, nodes):
        # deny access to the left tunnel
        nodes.denyAccessList(*(self.addOffset(2, 3) + (LEFT, ghosts)))
        # deny access to the right tunnel
        nodes.denyAccessList(*(self.addOffset(2, 3) + (RIGHT, ghosts)))

        # loop through the keys of the ghostNodeDeny dictionary
        for direction in list(self.ghostNodeDeny.keys()):
            # loop through the values for the current direction
            for values in self.ghostNodeDeny[direction]:
                # deny access to the given node for the specified direction
                nodes.denyAccessList(*(values + (direction, ghosts)))

# define a class for the first maze, which inherits from MazeBase
class Maze1(MazeBase):
    def setPortalPairs(self, nodes):
        for pair in list(self.portalPairs.values()):
            nodes.setPortalPair(*pair)

    def connectHomeNodes(self, nodes):
        key = nodes.createHomeNodes(*self.homeoffset)
        nodes.connectHomeNodes(key, self.homenodeconnectLeft, LEFT)
        nodes.connectHomeNodes(key, self.homenodeconnectRight, RIGHT)

    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze1"
        self.portalPairs = {0:((0, 17), (27, 17))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (12, 14)
        self.homenodeconnectRight = (15, 14)
        self.pacmanStart = (15, 26)
        self.fruitStart = (9, 20)
        self.ghostNodeDeny = {UP:((12, 14), (15, 14), (12, 26), (15, 26)), LEFT:(self.addOffset(2, 3),),
                              RIGHT:(self.addOffset(2, 3),)}

# define a class for the second maze, which also inherits from MazeBase
class Maze2(MazeBase):
    def setPortalPairs(self, nodes):
        for pair in list(self.portalPairs.values()):
            nodes.setPortalPair(*pair)

    def connectHomeNodes(self, nodes):
        key = nodes.createHomeNodes(*self.homeoffset)
        nodes.connectHomeNodes(key, self.homenodeconnectLeft, LEFT)
        nodes.connectHomeNodes(key, self.homenodeconnectRight, RIGHT)

    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze2"
        self.portalPairs = {0:((0, 4), (27, 4)), 1:((0, 26), (27, 26))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (9, 14)
        self.homenodeconnectRight = (18, 14)
        self.pacmanStart = (16, 26)
        self.fruitStart = (11, 20)
        self.ghostNodeDeny = {UP:((9, 14), (18, 14), (11, 23), (16, 23)), LEFT:(self.addOffset(2, 3),),
                              RIGHT:(self.addOffset(2, 3),)}

# Define a class MazeData
class MazeData(object):
    def __init__(self):
        self.obj = None
        self.mazedict = {0:Maze1, 1:Maze2}

    def loadMaze(self, level):
        self.obj = self.mazedict[level%len(self.mazedict)]()



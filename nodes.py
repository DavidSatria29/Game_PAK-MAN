import pygame
# Import necessary modules
from vector import Vector2
from constants import *
import numpy as np

# Define a class for a node in the game
class Node(object):
    def __init__(self, x, y):
        # Initialize the position of the node with a Vector2 object
        self.position = Vector2(x, y)
        
        # Define a dictionary to store neighboring nodes in each direction, initialized to None
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL:None}
        
        # Define a dictionary to store which entities (e.g. Pacman, Blinky, etc.) can move in each direction
        self.access = {UP:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT], 
                       DOWN:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT], 
                       LEFT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT], 
                       RIGHT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT]}
        
    # Method to deny access to a certain direction for a certain entity
    def denyAccess(self, direction, entity):
        # If the entity is currently allowed to move in the given direction, remove it from the list
        if entity.name in self.access[direction]:
            self.access[direction].remove(entity.name)
    
    # Method to allow access to a certain direction for a certain entity
    def allowAccess(self, direction, entity):
        # If the entity is not currently allowed to move in the given direction, add it to the list
        if entity.name not in self.access[direction]:
            self.access[direction].append(entity.name)
    
    # Method to render the node on the screen
    def render(self, screen):
        # Iterate through each neighbor of the node
        for n in self.neighbors.keys():
            # If the neighbor is not None (i.e. there is a connection to another node in this direction)
            if self.neighbors[n] is not None:
                # Draw a line between the center of this node and the center of the neighboring node
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                # Draw a red circle at the center of this node
                pygame.draw.circle(screen, RED, self.position.asInt(), 12)

class NodeGroup(object):
    def __init__(self, level):
        # Initializes a NodeGroup object with a given level
        self.level = level
        # Creates an empty dictionary to store nodes
        self.nodesLUT = {}
        # Specifies the symbols that represent nodes
        self.nodeSymbols = ['+', 'P', 'n']
        # Specifies the symbols that represent paths
        self.pathSymbols = ['.', '-', '|', 'p']
        # Reads the maze file and stores it as a numpy array
        data = self.readMazeFile(level)
        # Creates nodes for each node symbol in the maze and adds them to the nodesLUT dictionary
        self.createNodeTable(data)
        # Connects nodes horizontally
        self.connectHorizontally(data)
        # Connects nodes vertically
        self.connectVertically(data)
        # Initializes the homekey attribute to None
        self.homekey = None

    def readMazeFile(self, textfile):
        # Reads a maze file and returns it as a numpy array of characters
        return np.loadtxt(textfile, dtype='<U1')

    def createNodeTable(self, data, xoffset=0, yoffset=0):
        # Creates nodes for each node symbol in the maze and adds them to the nodesLUT dictionary
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col+xoffset, row+yoffset)
                    self.nodesLUT[(x, y)] = Node(x, y)

    def constructKey(self, x, y):
        # Constructs a tuple of (x, y) coordinates for a given position
        return x * TILEWIDTH, y * TILEHEIGHT


    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        # Connects nodes horizontally
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        # Connects the current node to the previous node
                        self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[LEFT] = self.nodesLUT[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    def connectVertically(self, data, xoffset=0, yoffset=0):
        # Connects nodes vertically
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        # Connects the current node to the previous node
                        self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[UP] = self.nodesLUT[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None


    def getStartTempNode(self):
        # Returns the first node in the node lookup table
        nodes = list(self.nodesLUT.values())
        return nodes[0]

    def setPortalPair(self, pair1, pair2):
        # Connects two nodes together as portals
        # Constructs keys from the two pairs
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        # If both keys are in the node lookup table, set each node's PORTAL neighbor to the other node
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]

    def createHomeNodes(self, xoffset, yoffset):
        # Creates a set of nodes in the shape of a house, with the top-left corner at the given x and y offsets
        homedata = np.array([['X','X','+','X','X'],
                            ['X','X','.','X','X'],
                            ['+','X','.','X','+'],
                            ['+','.','+','.','+'],
                            ['+','X','X','X','+']])
        # Creates nodes and connects them horizontally and vertically
        self.createNodeTable(homedata, xoffset, yoffset)
        self.connectHorizontally(homedata, xoffset, yoffset)
        self.connectVertically(homedata, xoffset, yoffset)
        # Sets the home key to the node located at (xoffset+2, yoffset) and returns the key
        self.homekey = self.constructKey(xoffset+2, yoffset)
        return self.homekey

    def connectHomeNodes(self, homekey, otherkey, direction):     
        # Connects a node specified by otherkey to the home node in the given direction (UP, DOWN, LEFT, or RIGHT)
        # Constructs a key from the otherkey
        key = self.constructKey(*otherkey)
        # Sets the home node's neighbor in the given direction to the node specified by otherkey, and vice versa
        self.nodesLUT[homekey].neighbors[direction] = self.nodesLUT[key]
        self.nodesLUT[key].neighbors[direction*-1] = self.nodesLUT[homekey]

    def getNodeFromPixels(self, xpixel, ypixel):
        # Returns the node at the given pixel coordinates, if it exists in the node lookup table
        if (xpixel, ypixel) in self.nodesLUT.keys():
            return self.nodesLUT[(xpixel, ypixel)]
        return None

    def getNodeFromTiles(self, col, row):
        # Returns the node at the given tile coordinates, if it exists in the node lookup table
        # Constructs a key from the col and row
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None

    def denyAccess(self, col, row, direction, entity):
        # Denies access to the node at the given tile coordinates from the given direction for the given entity
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.denyAccess(direction, entity)

    def allowAccess(self, col, row, direction, entity):
        node = self.getNodeFromTiles(col, row)  # Get the node corresponding to the specified col and row
        if node is not None:
            node.allowAccess(direction, entity)  # Allow access for the specified direction and entity

    def denyAccessList(self, col, row, direction, entities):
        for entity in entities:
            self.denyAccess(col, row, direction, entity)  # Loop through the entities and deny access for each one

    def allowAccessList(self, col, row, direction, entities):
        for entity in entities:
            self.allowAccess(col, row, direction, entity)  # Loop through the entities and allow access for each one

    def denyHomeAccess(self, entity):
        self.nodesLUT[self.homekey].denyAccess(DOWN, entity)  # Deny access to the home node for the specified entity

    def allowHomeAccess(self, entity):
        self.nodesLUT[self.homekey].allowAccess(DOWN, entity)  # Allow access to the home node for the specified entity

    def denyHomeAccessList(self, entities):
        for entity in entities:
            self.denyHomeAccess(entity)  # Loop through the entities and deny access to the home node for each one

    def allowHomeAccessList(self, entities):
        for entity in entities:
            self.allowHomeAccess(entity)  # Loop through the entities and allow access to the home node for each one

    def render(self, screen):
        for node in self.nodesLUT.values():
            node.render(screen)  # Render all the nodes in the level on the specified screen

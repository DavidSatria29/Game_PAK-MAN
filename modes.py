from constants import *

class MainMode(object):
    def __init__(self):
        # Initialize timer and start with scatter mode
        self.timer = 0
        self.scatter()

    def update(self, dt):
        # Update timer and check if it's time to switch modes
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()

    def scatter(self):
        # Set mode to scatter and reset timer
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        # Set mode to chase and reset timer
        self.mode = CHASE
        self.time = 20
        self.timer = 0


class ModeController(object):
    def __init__(self, entity):
        # Initialize timer, main mode, current mode, and entity
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity 

    def update(self, dt):
        # Update main mode and check if the current mode should switch
        self.mainmode.update(dt)
        if self.current is FREIGHT:
            # If in freight mode, update timer and check if it's time to switch back to normal mode
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                self.entity.normalMode()
                self.current = self.mainmode.mode
        elif self.current in [SCATTER, CHASE]:
            # If in scatter or chase mode, update current mode to match main mode
            self.current = self.mainmode.mode

        if self.current is SPAWN:
            # If in spawn mode and the entity has reached its spawn node, switch back to normal mode
            if self.entity.node == self.entity.spawnNode:
                self.entity.normalMode()
                self.current = self.mainmode.mode

    def setFreightMode(self):
        # Set mode to freight and reset timer if not already in freight mode
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 7
            self.current = FREIGHT
        elif self.current is FREIGHT:
            self.timer = 0

    def setSpawnMode(self):
        # Set mode to spawn if currently in freight mode
        if self.current is FREIGHT:
            self.current = SPAWN

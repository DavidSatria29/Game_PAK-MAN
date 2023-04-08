class Pause(object):
    def __init__(self, paused=False):
        # Initialize the object with a default pause status of False
        self.paused = paused
        # Set a timer for tracking how long the object has been paused
        self.timer = 0
        # Set a variable for storing the duration of the current pause
        self.pauseTime = None
        # Set a variable for storing a function to be executed after the pause
        self.func = None
        
    def update(self, dt):
        # This method is called on every update loop to check if the pause has ended
        if self.pauseTime is not None:
            # If the object is currently paused, update the timer with the elapsed time since the last update
            self.timer += dt
            # If the timer has exceeded the pause duration, reset the timer, unpause the object, and return the stored function (if any)
            if self.timer >= self.pauseTime:
                self.timer = 0
                self.paused = False
                self.pauseTime = None
                return self.func
        # If the object is not paused or the pause duration has not yet elapsed, return None
        return None

    def setPause(self, playerPaused=False, pauseTime=None, func=None):
        # This method is called to initiate a pause
        # It takes three optional arguments: 
        # playerPaused (default False) can be used to override the current pause status of the object
        # pauseTime (default None) specifies how long the pause should last
        # func (default None) is a function that will be executed after the pause has ended
        self.timer = 0
        self.func = func
        self.pauseTime = pauseTime
        self.flip()

    def flip(self):
        # This method is called to toggle the pause status of the object
        self.paused = not self.paused

# Importing constants module in order to use its variables
from constants import *

# Defining an Animator class
class Animator:
    # Constructor method for the Animator class
    def __init__(self, frames=(), speed=20, loop=True):
        # Initializing instance variables
        self.frames = frames  # A tuple of animation frames
        self.num_frames = len(frames)  # The number of frames in the animation
        self.current_frame = 0  # The current frame being displayed
        self.speed = speed  # The speed at which the animation is played (frames per second)
        self.loop = loop  # Whether the animation should loop or not
        self.dt = 0  # The time since the last frame change, initialized to 0
        self.finished = False  # Whether the animation has finished playing, initialized to False

    # Resetting the animation to its initial state
    def reset(self):
        self.current_frame = 0  # Setting the current frame to the first frame
        self.finished = False  # Setting the finished flag to False

    # Updating the animation with the time elapsed since the last update
    def update(self, dt):
        if not self.finished:
            self.next_frame(dt)  # Moving to the next frame if the animation hasn't finished
        # Checking if the animation has reached the end
        if self.current_frame == self.num_frames:
            # Checking if the animation should loop
            if self.loop:
                self.current_frame = 0  # Starting the animation from the beginning
            else:
                self.finished = True  # Marking the animation as finished
                self.current_frame -= 1  # Reverting back to the last frame displayed
        
        # Returning the current frame of the animation
        return self.frames[self.current_frame]

    # Advancing to the next frame if enough time has elapsed
    def next_frame(self, dt):
        self.dt += dt  # Adding the time elapsed since the last update to the delta time
        # Checking if enough time has elapsed to move to the next frame
        if self.dt >= (1.0 / self.speed):
            self.current_frame += 1  # Advancing to the next frame
            self.dt = 0  # Resetting the delta time to 0





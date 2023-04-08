# Import the math module to use mathematical functions such as sqrt()
import math

# Define a Vector2 class to create 2D vectors with x and y components
class Vector2(object):
    def __init__(self, x=0, y=0):
        # Initialize the x and y components
        self.x = x
        self.y = y
        # Set a threshold value for checking equality between vectors
        self.thresh = 0.000001

    # Define addition of two Vectors
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    # Define subtraction of two Vectors
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    # Define negation of a Vector
    def __neg__(self):
        return Vector2(-self.x, -self.y)

    # Define multiplication of a Vector by a scalar
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    # Define division of a Vector by a scalar
    def __div__(self, scalar):
        if scalar != 0:
            return Vector2(self.x / float(scalar), self.y / float(scalar))
        return None

    # Define true division of a Vector by a scalar
    def __truediv__(self, scalar):
        return self.__div__(scalar)

    # Define equality of two Vectors
    def __eq__(self, other):
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False

    # Calculate the squared magnitude of the Vector
    def magnitudeSquared(self):
        return self.x**2 + self.y**2

    # Calculate the magnitude of the Vector
    def magnitude(self):
        return math.sqrt(self.magnitudeSquared())

    # Create a copy of the current Vector
    def copy(self):
        return Vector2(self.x, self.y)

    # Convert the Vector to a tuple
    def asTuple(self):
        return self.x, self.y

    # Convert the Vector components to integers and return as a tuple
    def asInt(self):
        return int(self.x), int(self.y)

    # Define a string representation of the Vector for printing/debugging purposes
    def __str__(self):
        return "<"+str(self.x)+", "+str(self.y)+">"

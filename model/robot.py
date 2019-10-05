import math

class robot:
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.position_x = None
        self.position_y = None
        self.velocity_x = None
        self.velocity_y = None
        self.theta = None

    def setPosition(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y

    def setVelocity(self, last_position_x, last_position_y, position_x, position_y):
        self.velocity_x = position_x - last_position_x
        self.velocity_y = position_y - last_position_y

    def calcTheta(self):
        self.theta = math.arctan(self.velocity_y, self.velocity_x)



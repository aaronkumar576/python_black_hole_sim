import math

class Camera:
    def __init__(self, speed=5.0):
        self.position = [0.0, 1.0, 20.0]
        self.rotation = [-90.0, -10.0]
        self.speed = speed
        self.free_mode = True 

    def toggle_free_mode(self):
        self.free_mode = not self.free_mode 

    def move_forward(self, distance):
        if self.free_mode:
            self.position[0] += distance * self.speed * math.cos(math.radians(self.rotation[0]))
            self.position[1] += distance * self.speed * math.sin(math.radians(self.rotation[1]))
            self.position[2] += distance * self.speed * math.sin(math.radians(self.rotation[0]))
            
    def move_backward(self, distance):
        if self.free_mode:
            self.position[0] -= distance * self.speed * math.cos(math.radians(self.rotation[0]))
            self.position[1] -= distance * self.speed * math.sin(math.radians(self.rotation[1]))
            self.position[2] -= distance * self.speed * math.sin(math.radians(self.rotation[0]))
            
    def strafe_left(self, distance):
        if self.free_mode:
            self.position[2] -= distance * self.speed * math.cos(math.radians(self.rotation[0]))
            self.position[0] += distance * self.speed * math.sin(math.radians(self.rotation[0]))

    def strafe_right(self, distance):
        if self.free_mode:
            self.position[2] += distance * self.speed * math.cos(math.radians(self.rotation[0]))
            self.position[0] -= distance * self.speed * math.sin(math.radians(self.rotation[0]))

    def rotate(self, dx, dy, sensitivity=0.1):
        if self.free_mode:
            dx *= sensitivity
            dy *= sensitivity
            self.rotation[0] += dx
            self.rotation[1] -= dy

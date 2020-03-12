from easytello import Tello
from time import sleep


HEIGHT = 50


class DroneGuider:
    
    def __init__(self):
        self.drone = Tello()
    
    def first_step(self):
        self.drone.takeoff()
        sleep(3)
        self.drone.up(HEIGHT)
        sleep(3)
    
    def step(self):
        self.drone.left(50)
        sleep(3)
    
    def get_stream(self):
        stream = master_drone.get_video_stream()
        return stream
from easytello import Tello
from time import sleep


from config import WAITING_TIME


class DroneGuider:
    
    def __init__(self, wanted_height, step_left):
        self.drone = Tello()
        self.wanted_height = wanted_height
        self.step_left = step_left
    
    def first_step(self):
        self.drone.takeoff()
        sleep(WAITING_TIME)
        height = 0.1*self.drone.get_height()
        sleep(WAITING_TIME)
        if self.wanted_height < height:
            self.drone.down((height - self.wanted_height)*100)
        else:
            self.drone.up((self.wanted_height - height)*100)
        sleep(WAITING_TIME)
    
    def step(self):
        self.drone.left(self.step_left*100)
        sleep(WAITING_TIME)
        height = 0.1*self.drone.get_height()
        sleep(WAITING_TIME)
        if self.wanted_height < height:
            self.drone.down((height - self.wanted_height)*100)
        else:
            self.drone.up((self.wanted_height - height)*100)
        sleep(WAITING_TIME)
    
    def get_stream(self):
        stream = master_drone.get_video_stream()
        return stream
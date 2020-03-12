from easytello import Tello
from time import sleep
import cv2

from mapping import Mapping


HEIGHT = 50


def main():
    
    mapper = Mapping()
    
    master_drone = Tello()
    master_drone.takeoff()
    
    sleep(3)
    
    master_drone.up(HEIGHT)
    
    sleep(3)
    
    height = master_drone.get_height()
    print("la hauteur est de " + str(height))
            
    sleep(3)
    
    stream = master_drone.get_video_stream()
    
    sleep(3)
    
    map = mapper.map(stream, height)
    
    master_drone.land()
    print(master_drone.get_battery())

main()


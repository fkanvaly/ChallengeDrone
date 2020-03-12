from easytello import Tello
from time import sleep
import cv2

from mapping import Mapping
from detection import YOLODetector
from server import Server
from drone_guiding import DroneGuider

from config import WAITING_TIME


DRONE_HEIGHT = 5


def main():
    
    drone_guider = DroneGuider(DRONE_HEIGHT, step_left=5)
    
    my_server = Server()
    mapper = Mapping()
    detector = YOLODetector()
    
    drone_guider.first_step()
    
    stream = drone_guider.get_stream()
    
    while True:
        
        drone_guider.step()
        height = 0.1 * drone_guider.drone.get_height()
        
        sleep(WAITING_TIME)
        
        ret, frame = stream.read()
        
        objects = detector(frame)
        map = mapper.map(frame, height)
        binded_map = map.bind(objects)
        my_server.post(binded_map)

    sleep(3)
        
    master_drone.land()
    print(master_drone.get_battery())

if __name__ == '__main__':
    main()
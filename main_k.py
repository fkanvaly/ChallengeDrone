from easytello import Tello
from time import sleep
import cv2

from src.mapping import Mapping
from src.detection import YOLODetector
from src.server import Server
from src.drone_guiding import DroneGuider
from src.cluster import Cluster
from src.client import Client

from config import WAITING_TIME, DRONE_HEIGHT, IP_K, IP_T, IP_Y

def parse_frame(frame):
    objects = detector(frame)
    map = mapper.map(frame, height)
    binded_map = map.bind(objects)
    positions = binded_map.find_positions()
    my_cluster = Cluster(positions)
    my_cluster.send_command(tom, yahya)
    
def parse(message):
    filename = message.split()[2]
    if filename.split('_')[0] == 'img':
        frame = cv2.imread(filename)
        cv2.imshow(frame)
    else:
        frame = cv2.imread(filename)
        parse_frame(frame)
        
kanva = Server(IP_K,1234)
    
_thread.start_new_thread(kanva.start, ())

drone_guider = DroneGuider(DRONE_HEIGHT, step_left=5)

mapper = Mapping()
detector = YOLODetector()

drone_guider.first_step()

stream = drone_guider.get_stream()

tom = Client(IP_T, 1234, 1)
yahya = Client(IP_Y, 1234, 1)

while True:
    drone_guider.step()
    height = 0.1 * drone_guider.drone.get_height()
    
    sleep(WAITING_TIME)
    
    ret, frame = stream.read()
    
    parse_frame(frame)
    
    if len(kanva.Received_messages) != 0:
        message = kanva.Received_messages.pop(0)
    if message.split()[0] == 'sending_image':
        parse(message)
    
sleep(3)
    
master_drone.land()
print(master_drone.get_battery())

if __name__ == '__main__':
    main()
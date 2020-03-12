from src.client import Client
from src.server import Server
from src.drone_guiding import DroneGuider
import _thread
from src.My_drone import My_drone
from time import sleep
import numpy
import cv2


from config import IP_K, IP_M, IP_T, IP_Y, DRONE_HEIGHT

### Possible messages : 
    # 'go x y'
    # 

def main():
    
    kanvaly_client = Client(IP_K,1234,1) #kanvaly.send_message ou #kanvaly.send_img pour envoyer à kanva
    
    drone_guider = DroneGuider(DRONE_HEIGHT, step_left=5)
    
    drone_guider.first_step()
    
    stream = drone_guider.get_stream()
    
    image_counter = 0
    
    while True:
        
        drone_guider.step()
        height = 0.1 * drone_guider.drone.get_height()
        
        sleep(WAITING_TIME)
        
        ret = False
        while not ret:
            
            ret, frame = stream.read()
        
        cv2.imwrite(str(image_counter) + ".png", frame)
        kanvaly_client.send_img(str(image_counter) + ".png")
        kanvaly_client.send_message(str(height))
        image_counter += 1

    sleep(3)
        
    master_drone.land()
    print(master_drone.get_battery())

if __name__ == '__main__':
    main()
        
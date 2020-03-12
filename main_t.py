from client import Client
from server import Server
import _thread
from My_drone import My_drone
from time import sleep
import numpy
import cv2
from config import IP_K, IP_T

kanva_ip = IP_K
kanvaly = Client(kanva_ip,1234,1) #kanvaly.send_message ou #kanvaly.send_img pour envoyer à kanva

tom_ip = IP_T
tom = Server(tom_ip,1234)

x0 = 0
y0 = 0
z0 = 499
my_drone = My_drone(x0,y0)
my_drone.take_off(z0)

try:
    _thread.start_new_thread(tom.start, ())
except:
    print("Error: unable to start thread")

### Possible messages : 
    # 'go x y'
    # 
def parse(message):
    if message.split()[0] == 'go':
        x = message.split()[1]
        y = message.split()[2]
        my_drone.go_to((x,y))
        frame = my_drone.take_picture()
        cv2.imwrite("img_(%s,%s).png" %(x,y), frame)
        kanvaly.send_img("img_(%s,%s).png" %(x,y))

while True:
    if len(tom.Received_messages) != 0:
        message = tom.Received_messages.pop(0)
        parse(message)

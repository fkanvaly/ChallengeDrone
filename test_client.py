from src.client import Client
import numpy as np
import cv2

from config import IP_K

my_client = Client(IP_K, 1234, 1)

frame = np.zeros((640,480,3))

cv2.imwrite("0.png", frame)
my_client.send_img("0.png")

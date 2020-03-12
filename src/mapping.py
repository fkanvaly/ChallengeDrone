import numpy as np
import cv2

class Map2D:
    
    def __init__(self):
        H, W = 720, 1280
        
        horizon_height = 0.848 * H
        down_width = 15
        
        b_l = [H, 0]
        b_r = [H, W]

        u = 10
        tetha = np.pi/2 - np.arctan((2*horizon_height)/W)
        x = np.tan(tetha) * u
        t_l = [H-horizon_height+u, W/2-x]
        t_r = [H-horizon_height+u, W/2+x]
        
        kp = np.array([t_r,t_l, b_r, b_l])
        
        map_h, map_w = 255,255
        map_points = np.array([0,0],[0,map_w],[map_h,map_w])
        
        self.H = cv2.findHomography(map_points, kp)
    
    def project(self, img):
        
from easytello import tello
import time

class My_drone:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.drone=tello.Tello()
        self.stream=self.drone.get_stream()

    def take_off(self,z):
        self.drone.take_off()
        self.drone.up(z)
        
    def update_pos(self, pos):
        self.x=pos[0]
        self.y=pos[1]

    def go_to(self, dest):
        move_x=dest[0]-self.x
        move_y=dest[1]-self.y
        
        for i in range(abs(move_x)//500):
            if move_x>=0:
                self.drone.right(500)
            if move_x<0:
                self.drone.left(500)
        
        if abs(move_x)%500>20:
            if move_x>=0:
                    self.drone.right(abs(move_x)%500)
            if move_x<0:
                self.drone.left(abs(move_x)%500)
            self.update_pos(dest)

        for i in range(abs(move_y)//500):
            if move_y>=0:
                self.drone.forward(500)
            if move_y<0:
                self.drone.back(500)
        
        if abs(move_y)%500>20:
            if move_y>=0:
                    self.drone.forward(abs(move_y)%500)
            if move_y<0:
                self.drone.back(abs(move_y)%500)

        self.update_pos(dest)

    def take_picture(self):
        ret,frame=self.stream.read()
        while not ret:
            ret, frame=self.stream.read()
            time.sleep()
        return frame


   
        

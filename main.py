from djitellopy import Tello

def main():
    
    master_drone = Tello()
    master_drone.connect()
    master_drone.takeoff()
    
    master_drone.move_up(50)
    height = master_drone.get_height()
     
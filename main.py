import time
import cv2
from djitellopy import Tello

from drone_controller import DroneController

def main():  
    time.sleep(5)
    drone = DroneController()
    drone.connect_and_setup()
    drone.takeoff()
    whileCount = 0

    while True:
        whileCount += 1
        if whileCount % 100 == 0:
            print("whileCount: ")
        if drone.check_for_quit():
            break
        img = drone.get_frame()
        cv2.imshow("Drone Camera", img)

    print("exited while loop")
    drone.land()

if __name__ == "__main__":
    main()

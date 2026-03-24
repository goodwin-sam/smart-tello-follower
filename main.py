import time
import cv2
from djitellopy import Tello

def main():
    tello = Tello()
    tello.connect()
    print("Battery: ", tello.get_battery())
    tello.streamon()
    cv2.waitKey(1000)    
    tello.takeoff()
    cv2.waitKey(1000)

    while True:
        print("entered while loop")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Landing...")
            break
        img = tello.get_frame_read().frame
        cv2.imshow("Drone Camera", img)
        cv2.waitKey(1)

    print("exited while loop")
    tello.land()

if __name__ == "__main__":
    main()

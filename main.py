import time
import cv2
from djitellopy import Tello
import face_recognition

from drone_controller import DroneController
from face_recognizer import FaceRecognizer

def main():  
    time.sleep(5)
    face_recognizer = FaceRecognizer("ref_img.jpg")

    drone = DroneController()
    drone.connect_and_setup()
    drone.takeoff()
    whileCount = 0

    while True:
        whileCount += 1
        if whileCount % 100 == 0:
            print("whileCount: " + str(whileCount))
        if drone.check_for_quit():
            break
        img = drone.get_frame()
        face_locations, face_matches = face_recognizer.recognize_faces(img)
        img = face_recognizer.draw_faces(img, face_locations, face_matches)
        cv2.imshow("Drone Camera", img)
        

    print("exited while loop")
    drone.land()

if __name__ == "__main__":
    main()

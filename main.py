import os

# Suppress harmless OpenCV/Qt warnings
os.environ["QT_QPA_PLATFORM"] = "xcb"
os.environ["QT_LOGGING_RULES"] = "*.debug=false;*.info=false;*.warning=false" 

import time
import cv2

from drone_controller import DroneController
from face_recognizer import FaceRecognizer
from gesture_recognizer import GestureRecognizer


def main():  
    """
    main entry point for the Smart Tello Drone system

    combines face tracking, following, and gesture control
    press "q" to quit the program and land the drone
    """
    drone = DroneController()
    face_recognizer = FaceRecognizer()
    gesture_recognizer = GestureRecognizer()

    try:
        drone.setup()
        drone.takeoff()

        while True:
            # check for quit
            if drone.check_for_quit():
                break

            # gets frame from drone
            img = drone.get_frame()
            img = cv2.flip(img, 1)

            # face recognition and visualization
            face_locations, face_matches = face_recognizer.recognize_faces(img)
            img = face_recognizer.draw_faces(img, face_locations, face_matches)

            # gesture recognition and response
            img, confirmed_gesture = gesture_recognizer.process_hands(img)
            if confirmed_gesture:
                drone.execute_gesture(confirmed_gesture)

            # movement control
            if drone.is_paused:
                drone.tello.send_rc_control(0, 0, 0, 0)
            else:
                # finds first matched face and follows it
                matched_face = drone.find_matched_face(face_locations, face_matches)
                drone.follow_matched_face(matched_face)

            # stream video feed
            cv2.imshow("Drone Camera", img)

            time.sleep(0.03)

    
    except KeyboardInterrupt:
        print("Keyboard interrupt detected (ctrl+c). shutting down...")

    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        print("Cleaning up and landing drone...")
        drone.land()
        drone.tello.streamoff()
        cv2.destroyAllWindows()
        print("Drone landed and windows closed")

if __name__ == "__main__":
    main()

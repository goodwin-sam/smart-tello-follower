import cv2
import mediapipe as mp
from collections import deque


class GestureRecognizer:
    """
    class for handling hand gesture recognition using MediaPipe
    with confirmation system to reduce false positives
    """

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.4, min_tracking_confidence=0.3)
        self.mp_draw = mp.solutions.drawing_utils

        # gesture confirmation settings
        self.GESTURE_CONFIRMATION_FRAMES = 20
        self.GESTURE_HISTORY = deque(maxlen=self.GESTURE_CONFIRMATION_FRAMES)
        self.GESTURE_COOLDOWN = 30
        self.cooldown_counter = 0
        

    def process_hands(self, img):
        """process hands, draw landmarks, and return confirmed gesture if detected"""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        hand_results = self.hands.process(img_rgb)
        confirmed_gesture = None

        if hand_results.multi_hand_landmarks:
            for i, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
                # draw hand landmarks
                self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                handedness = hand_results.multi_handedness[i].classification[0].label
                finger_count = self.get_finger_count(hand_landmarks, handedness)
                gesture = self.get_gesture(finger_count, hand_landmarks)

                self.GESTURE_HISTORY.append(gesture)
                confirmed_gesture = self.get_confirmed_gesture()

                # display gesture feedback on stream
                if gesture:
                    self._draw_gesture_label(img, hand_landmarks, gesture, confirmed_gesture)

        else:
            self.GESTURE_HISTORY.clear()
        
        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1

        return img, confirmed_gesture
    

    def _draw_gesture_label(self, img, hand_landmarks, gesture, confirmed_gesture):
        """draw gesture text on stream"""
        wrist = hand_landmarks.landmark[0]
        label_x = int(wrist.x*img.shape[1])
        label_y = int(wrist.y*img.shape[0])+20

        if confirmed_gesture and self.cooldown_counter == 0:
            self.cooldown_counter = self.GESTURE_COOLDOWN
            cv2.putText(img, f"Confirmed: {confirmed_gesture}", (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 3)
        elif confirmed_gesture and self.cooldown_counter > 0:
            cv2.putText(img, f"Confirmed: {confirmed_gesture}", (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 3)
        elif gesture and self.cooldown_counter == 0:
            cv2.putText(img, f"Unconfirmed Gesture: {gesture}", (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)

    
    def get_finger_count(self, hand_landmarks, handedness):
        """count extended fingers"""
        landmarks = hand_landmarks.landmark
        extended_fingers = 0

        # thumb
        if handedness == "Left":
            if landmarks[4].x > landmarks[3].x:
                 extended_fingers += 1
        elif handedness == "Right":
            if landmarks[4].x < landmarks[3].x:
                extended_fingers += 1

        # four fingers
        for tip, mid in [(8, 6), (12, 10), (16, 14), (20, 18)]:
            if landmarks[tip].y < landmarks[mid].y:
                extended_fingers += 1

        return extended_fingers
        

    def is_ok_sign(self, landmarks):
        """detect OK sign"""
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]

        pinch_distance = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5
        pinching = pinch_distance < 0.07

        other_fingers_extended = all(landmarks[tip].y < landmarks[mid].y for tip, mid in [(12, 10), (16, 14), (20, 18)])

        return pinching and other_fingers_extended


    def get_confirmed_gesture(self):
        """confirm gesture has enough consistent frames"""
        if len(self.GESTURE_HISTORY) < self.GESTURE_CONFIRMATION_FRAMES:
            return None
        
        first_gesture = self.GESTURE_HISTORY[0]
        if all(gesture == first_gesture for gesture in self.GESTURE_HISTORY):
            return first_gesture
        return None


    def get_gesture(self, finger_count, hand_landmarks):
        """map finger count and other characteristics to specific gestures"""
        if self.is_ok_sign(hand_landmarks.landmark):
            return "OK"
        elif finger_count == 0:
            return "Fist"
        elif finger_count == 1:
            return "One_Finger"
        elif finger_count == 2:
            return "Two_Fingers"
        elif finger_count == 3:
            return "Three_Fingers"
        elif finger_count == 4:
            return "Four_Fingers"
        elif finger_count == 5:
            return "Open_Palm"
        else:
            return None
            

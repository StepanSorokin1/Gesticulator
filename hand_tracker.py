import mediapipe as mp
import cv2
from constants import MEDIAPIPE_CONFIG

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(**MEDIAPIPE_CONFIG)
        self.mp_draw = mp.solutions.drawing_utils
    
    def process(self, frame):
        # Конвертируем BGR в RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        landmarks = None
        handedness = None
        
        if results.multi_hand_landmarks:
            # Берем первую обнаруженную руку
            landmarks = results.multi_hand_landmarks[0].landmark
            handedness = results.multi_handedness[0].classification[0].label
            
            # Рисуем landmarks (опционально)
            # self.mp_draw.draw_landmarks(frame, results.multi_hand_landmarks[0])
        
        return landmarks, handedness
    
    def close(self):
        self.hands.close()
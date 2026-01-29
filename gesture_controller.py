from mouse import MouseController
from gesture_tracker import GestureDetector

class GestureController:
    def __init__(self):
        self.mouse = MouseController()
        self.last_gesture = None
    
    def handle_gesture(self, gesture, landmarks, handedness):
        """Обрабатывает жест"""
        if gesture == "POINT" and landmarks:
            self.mouse.move(landmarks[8].x*1.7 - 0.3, landmarks[8].y*1.7)
        
        elif gesture == "VICTORY":
            self.mouse.click()
        
        elif gesture == "ROCK":
            self.mouse.right_click()
        
        self.last_gesture = gesture
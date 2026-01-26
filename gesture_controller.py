from mouse import MouseController
from gesture_tracker import GestureDetector

class GestureController:
    def __init__(self):
        self.mouse = MouseController()
        self.last_gesture = None
    
    def handle_gesture(self, gesture, landmarks, handedness):
        """Обрабатывает жест"""
        if gesture == "POINT" and landmarks:
            # Управление мышью указательным пальцем
            self.mouse.move(landmarks[8].x, landmarks[8].y)
        
        elif gesture == "FIST" and self.last_gesture != "FIST":
            # Клик при сжатии кулака
            self.mouse.click()
        
        elif gesture == "VICTORY" and self.last_gesture != "VICTORY":
            # Двойной клик жестом "V"
            self.mouse.double_click()
        
        elif gesture == "OPEN_HAND" and self.last_gesture != "OPEN_HAND":
            # Правый клик открытой ладонью
            self.mouse.right_click()
        
        self.last_gesture = gesture
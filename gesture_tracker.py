from constants import *

class GestureDetector:
    @staticmethod
    def get_fingers_up(landmarks, handedness):
        """Определяет, какие пальцы подняты"""
        fingers = {
            'thumb': False,
            'index': False,
            'middle': False,
            'ring': False,
            'pinky': False
        }
        
        # Простая логика: палец поднят, если его кончик выше сустава
        fingers['index'] = landmarks[INDEX_TIP].y < landmarks[INDEX_TIP-2].y
        fingers['middle'] = landmarks[MIDDLE_TIP].y < landmarks[MIDDLE_TIP-2].y
        fingers['ring'] = landmarks[RING_TIP].y < landmarks[RING_TIP-2].y
        fingers['pinky'] = landmarks[PINKY_TIP].y < landmarks[PINKY_TIP-2].y
        
        # Большой палец - отдельная логика
        if handedness == "Right":
            fingers['thumb'] = landmarks[THUMB_TIP].x > landmarks[THUMB_TIP-1].x
        else:
            fingers['thumb'] = landmarks[THUMB_TIP].x < landmarks[THUMB_TIP-1].x
        
        return fingers
    
    @staticmethod
    def detect_gesture(fingers):
        """Определяет жест по положению пальцев"""
        # Указательный палец поднят, остальные опущены
        if fingers['index'] and not any([fingers['middle'], fingers['ring'], fingers['pinky']]):
            return "POINT"
        
        # Все пальцы подняты
        if all(fingers.values()):
            return "OPEN_HAND"
        
        # Все пальцы опущены
        if not any(fingers.values()):
            return "FIST"
        
        # Указательный и средний подняты (жест "V")
        if fingers['index'] and fingers['middle'] and not fingers['ring'] and not fingers['pinky']:
            return "VICTORY"
        
        if not fingers['thumb'] and all([fingers['index'], fingers['middle'], fingers['ring'], fingers['pinky']]):
            return "STOP"
        
        return "UNKNOWN"
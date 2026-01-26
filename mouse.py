import pyautogui
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MOUSE_SMOOTHING

class MouseController:
    def __init__(self):
        self.prev_x, self.prev_y = None, None
    
    def move(self, x, y):
        """Плавное перемещение мыши"""
        # Конвертируем координаты в пиксели экрана
        screen_x = int(x * SCREEN_WIDTH)
        screen_y = int(y * SCREEN_HEIGHT)
        
        # Применяем сглаживание
        if self.prev_x is None:
            self.prev_x, self.prev_y = screen_x, screen_y
        
        smooth_x = int(self.prev_x * (1 - MOUSE_SMOOTHING) + screen_x * MOUSE_SMOOTHING)
        smooth_y = int(self.prev_y * (1 - MOUSE_SMOOTHING) + screen_y * MOUSE_SMOOTHING)
        
        pyautogui.moveTo(smooth_x, smooth_y)
        self.prev_x, self.prev_y = smooth_x, smooth_y
    
    def click(self):
        pyautogui.click()
    
    def double_click(self):
        pyautogui.doubleClick()
    
    def right_click(self):
        pyautogui.rightClick()


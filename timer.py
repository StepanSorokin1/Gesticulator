from time import time
from constants import *

class Timer():
    def __init__(self):
        self.frame_counter = 0
        self.next_time = 0
        self.prev_time = 0
        self.FPS = 0
    def FPS_counter(self):
        self.frame_counter += 1
        self.next_time = time()
        if self.next_time - self.prev_time >= INTERVAL:
            self.FPS = self.frame_counter // (self.next_time - self.prev_time)
            self.prev_time = self.next_time
            self.frame_counter = 0
        return self.FPS
        
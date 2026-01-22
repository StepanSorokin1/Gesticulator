import cv2 as cv
from time import time

cap = cv.VideoCapture(0)
prev_time = 0
fps = 0
interval = 0.25
frame_counter = 0

while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        

        cv.imshow('check', frame)

        

cap.release()
cv.destroyAllWindows()
import pyautogui as gui



def move_mouse(x, y):
    gui.moveTo(x, y)

def get_hand_information(results, landmarks):    
    

    handedness = None
    direction = None
    side = None

    if results.classification[0].label == "Right":
        handedness = "Right"
        if landmarks[0].y < landmarks[5].y and landmarks[0].y < landmarks[17].y:
            direction = "Up"
            if landmarks[0].x < landmarks[1].x:
                side = "In"
            else:
                side = "Out"
        
        elif landmarks[0].y > landmarks[5].y and landmarks[0].y > landmarks[17].y:
            direction = "Down"
            if landmarks[1].x < landmarks[0].x:
                side = "In"
            else:
                side = "Out"
        
        elif landmarks[5].x < landmarks[0].x:
            direction = "Left"
            if landmarks[17].y < landmarks[0].y < landmarks[5].y:
                side = "In"
            else:
                side = "Out"
        
        elif landmarks[0].x < landmarks[5].x:
            direction = "Right"
            if landmarks[17].y > landmarks[0].y > landmarks[5].y:
                side = "In"
            else:
                side = "Out"
    
    elif results.classification[0].label == "Left":
        handedness = "Left"
        if landmarks[0].y < landmarks[5].y and landmarks[0].y < landmarks[17].y:
            direction = "Up"
            if landmarks[1].x < landmarks[0].x:
                side = "In"
            else:
                side = "Out"

        elif landmarks[0].y > landmarks[5].y and landmarks[0].y > landmarks[17].y:
            direction = "Down"
            if landmarks[0].x < landmarks[1].x:
                side = "In"
            else:
                side = "Out"
        
        elif landmarks[5].x < landmarks[0].x:
            direction = "Left"
            if landmarks[17].y > landmarks[0].y > landmarks[5].y:
                side = "In"
            else:
                side = "Out"

        elif landmarks[0].x < landmarks[5].x:
            direction = "Right"
            if landmarks[17].y < landmarks[0].y < landmarks[5].y:
                side = "In"
            else:
                side = "Out"

    return handedness, direction, side



def get_finger_state(handedness, direction, side, landmarks):
    """Определяет состояние пальцев (поднят/опущен) = (True/False)"""
    finger_states = {
        'thumb': False,
        'index': False,
        'middle': False,
        'ring': False,
        'pinky': False
    }
    
    if handedness == "Right":
        if direction == "Up":
            finger_states["index"] = landmarks[8].y > landmarks[7].y
            finger_states["middle"] = landmarks[12].y > landmarks[11].y
            finger_states["ring"] = landmarks[16].y > landmarks[15].y
            finger_states["pinky"] = landmarks[20].y > landmarks[19].y
            if side == "In":
                finger_states["thumb"] = landmarks[4].x > landmarks[3].x
            elif side == "Out":
                finger_states["thumb"] = landmarks[3].x > landmarks[4].x

        elif direction == "Down":
            finger_states["index"] = landmarks[8].y < landmarks[7].y
            finger_states["middle"] = landmarks[12].y < landmarks[11].y
            finger_states["ring"] = landmarks[16].y < landmarks[15].y
            finger_states["pinky"] = landmarks[20].y < landmarks[19].y
            if side == "In":
                finger_states["thumb"] = landmarks[3].x > landmarks[4].x 
            elif side == "Out":
                finger_states["thumb"] = landmarks[4].x > landmarks[3].x

        elif direction == "Right":
            finger_states["index"] = landmarks[7].x < landmarks[8].x
            finger_states["middle"] = landmarks[11].x < landmarks[12].x
            finger_states["ring"] = landmarks[15].x < landmarks[16].x
            finger_states["pinky"] = landmarks[19].x < landmarks[20].x
            if side == "In":
                finger_states["thumb"] = landmarks[3].y > landmarks[4].y
            elif side == "Out":
                finger_states["thumb"] = landmarks[4].y > landmarks[3].y
        
        elif direction == "Left":
            finger_states["index"] = landmarks[8].x < landmarks[7].x
            finger_states["middle"] = landmarks[12].x < landmarks[11].x
            finger_states["ring"] = landmarks[16].x < landmarks[15].x
            finger_states["pinky"] = landmarks[20].x < landmarks[19].x
            if side == "In":
                finger_states["thumb"] = landmarks[4].y > landmarks[3].y
            elif side == "Out":
                finger_states["thumb"] = landmarks[3].y > landmarks[4].y
    

    elif handedness == "Left":
        if direction == "Up":
            finger_states["index"] = landmarks[8].y > landmarks[7].y
            finger_states["middle"] = landmarks[12].y > landmarks[11].y
            finger_states["ring"] = landmarks[16].y > landmarks[15].y
            finger_states["pinky"] = landmarks[20].y > landmarks[19].y
            if side == "In":
                finger_states["thumb"] = landmarks[3].x > landmarks[4].x
            elif side == "Out":
                finger_states["thumb"] = landmarks[4].x > landmarks[3].x

        elif direction == "Down":
            finger_states["index"] = landmarks[8].y < landmarks[7].y
            finger_states["middle"] = landmarks[12].y < landmarks[11].y
            finger_states["ring"] = landmarks[16].y < landmarks[15].y
            finger_states["pinky"] = landmarks[20].y < landmarks[19].y
            if side == "In":
                finger_states["thumb"] = landmarks[4].x > landmarks[3].x 
            elif side == "Out":
                finger_states["thumb"] = landmarks[3].x > landmarks[4].x

        elif direction == "Right":
            finger_states["index"] = landmarks[7].x < landmarks[8].x
            finger_states["middle"] = landmarks[11].x < landmarks[12].x
            finger_states["ring"] = landmarks[15].x < landmarks[16].x
            finger_states["pinky"] = landmarks[19].x < landmarks[20].x
            if side == "In":
                finger_states["thumb"] = landmarks[4].y > landmarks[3].y
            elif side == "Out":
                finger_states["thumb"] = landmarks[3].y > landmarks[4].y
        
        elif direction == "Left":
            finger_states["index"] = landmarks[8].x < landmarks[7].x
            finger_states["middle"] = landmarks[12].x < landmarks[11].x
            finger_states["ring"] = landmarks[16].x < landmarks[15].x
            finger_states["pinky"] = landmarks[20].x < landmarks[19].x
            if side == "In":
                finger_states["thumb"] = landmarks[3].y > landmarks[4].y
            elif side == "Out":
                finger_states["thumb"] = landmarks[4].y > landmarks[3].y

    return finger_states



def recognize_gesture(handedness, direction, side, landmarks, finger_states):
    if side == "In" and direction =="Up":
        if finger_states["index"] and not any([finger_states["middle"], finger_states["ring"], finger_states["pinky"]]):
            return "Pointing_Up"
        if not finger_states["thumb"] and all([finger_states["index"], finger_states["middle"], finger_states["ring"], finger_states["pinky"]]):
            return "Stop"
        if not any([finger_states["thumb"], finger_states["index"], finger_states["middle"], finger_states["ring"], finger_states["pinky"]]):
            return "Fist"
    return None
    
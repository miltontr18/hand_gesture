def detect_gesture(fingers):
    thumb, index, middle, ring, pinky = fingers
    if sum(fingers) == 0:
        return 'S', "STOP"
    elif sum(fingers) == 1 and index:
        return 'B', "BACK"
    elif sum(fingers) == 2 and index and middle:
        return 'F', "FORWARD"
    elif sum(fingers) == 3 and middle and ring and pinky:
        return 'L', "STRAFE LEFT"
    elif sum(fingers) == 4 and not thumb:
        return 'R', "STRAFE RIGHT"
    elif thumb and pinky and not index and not middle and not ring:
        return 'Q', "ROTATE LEFT"
    elif index and pinky and not thumb and not middle and not ring:
        return 'E', "ROTATE RIGHT"
    else:
        return 'S', "IDLE"

def arm_pose(f):
    return (f[0] == 1 and f[1] == 1 and f[2] == 1 and f[3] == 0 and f[4] == 0)

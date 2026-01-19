import cv2
from config import settings

def init_camera():
    cap = cv2.VideoCapture(0)
    cap.set(3, settings.CAM_WIDTH)
    cap.set(4, settings.CAM_HEIGHT)
    return cap

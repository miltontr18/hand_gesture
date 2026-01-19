from config import settings
from network.esp32_socket import connect
from vision.camera import init_camera
from control.gesture_controller import run

def main():
    sock = connect(settings.ESP32_IP, settings.PORT)
    cap = init_camera()
    run(sock, cap)

if __name__ == "__main__":
    main()

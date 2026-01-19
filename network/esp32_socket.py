import socket

def connect(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    print(f"✅ Connected to ESP32 ({ip}:{port})")
    return sock

def safe_send(sock, char: str):
    try:
        sock.send(char.encode())
        print(f"➡️ Sent: {char}")
    except Exception as e:
        print("⚠️ Send error:", e)

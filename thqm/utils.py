import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # this sees if device is connected to internet
    ip = s.getsockname()[0]
    s.close()
    return ip

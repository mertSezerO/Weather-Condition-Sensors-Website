from client import client_TCP, client_UDP

class Gateway:
    def __init__(self, host, port):
        self.tcp_socket = client_TCP.ClientTCP(host=host, port=port).socket
        self.udp_socket = client_UDP.ClientUDP(host=host, port=port).socket

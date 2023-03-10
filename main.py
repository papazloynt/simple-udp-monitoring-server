import socket
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import start_http_server, Counter


graphs = {}
graphs['ok'] = Counter('ok', 'system in good state')
graphs['high_temp'] = Counter('high_temp', 'there are fire everywhere')
graphs['invasion'] = Counter('invasion', 'some person are there, call the police!!!')
graphs['power_off'] = Counter('power_off', 'you should check the state of your power')


class UDPServer:
    def __init__(self, ip_addr, port, buffer_size, bytes_to_send):
        self.buffer_size = buffer_size
        self.bytes_to_send = bytes_to_send
        # Create a datagram socket
        self.udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Bind to address and ip
        self.udp_server_socket.bind((ip_addr, port))
        print("UDP server up and listening")

    def get_message(self):
        bytes_address_pair = self.udp_server_socket.recvfrom(self.buffer_size)
        message, address = bytes_address_pair[0], bytes_address_pair[1]

        print("Message from Client: {}".format(str(message, 'utf-8')))
        print("Client IP Address: {}".format(address))

        self.udp_server_socket.sendto(self.bytes_to_send, address)
        return str(message, 'utf-8')


if __name__ == '__main__':
    udp_server = UDPServer("192.168.1.68", 10002, 1024, str.encode("I got your answer, poor baby"))
    start_http_server(8000)
    i = 0
    while True:
        received_msg = udp_server.get_message()
        # prometheus metrics
        if received_msg == 'OK':
            graphs['ok'].inc()
        elif 'temperature' in received_msg:
            graphs['high_temp'].inc()
        elif 'invasion' in received_msg:
            graphs['invasion'].inc()
        elif 'power off' in received_msg:
            graphs['power_off'].inc()

import socket

class UdpClient:
    def __init__(self, address = None, port = None):
        self.address = address if address is not None else 'localhost'
        self.port = port if port is not None else 9000
        self.server_address = (self.address, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connect(self):
        self.socket.connect(self.server_address)

    def send_text_message(self, msg):
        self.socket(msg.encode('utf-8'))

    def send_protobuf_message(self, msg):
        return self.socket.send(msg)

    def close(self):
        print("closing socket")
        self.socket.close()
        print("done")


class UdpServer:
    def __init__(self, address = None, port = None, callback = None, recv_buffer = 10000):
        self._address = address if address is not None else 'localhost'
        self._port = port if port is not None else 9000
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._callback = callback
        self._recv_buffer = recv_buffer
        self._socket.setblocking(False)

    def bind(self):
        self._socket.bind((self._address, self._port))

    def receive(self, callback):
        try:
            msg, _ = self._socket.recvfrom(self._recv_buffer)
            callback(msg)
        except BlockingIOError:
            pass
        except Exception as e:
            print(f"Error receiving data: {e}")

    def close(self):
        print("closing socket")
        self._socket.close()
        print("done")
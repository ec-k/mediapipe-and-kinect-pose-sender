import network.udp_client as udp_client
from holistic_landmarks_pb2 import HolisticLandmarks

class HolisticPoseSender:
    def __init__(self, address=None, port=None):
        self.client = udp_client.UdpClient(address, port)

    def connect(self):
        self.client.connect()

    def send_holistic_landmarks(self, holistic_results:HolisticLandmarks):
        """Send results with udp.

        Args:
            holistic_results (HolisticLandmarks): Packed results of MediaPipe Pose, Hands and Face.
        """
        msg = holistic_results.SerializeToString()
        return self.client.send_protobuf_message(msg)


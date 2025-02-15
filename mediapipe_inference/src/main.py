from network.holistic_pose_sender import HolisticPoseSender
from network.udp_client import UdpServer
from holistic_detector import HolisticDetector
import packer
import visualizer
import cv2
import mediapipe as mp
import numpy as np
import time
from pathlib import Path
from holistic_landmarks_pb2 import HolisticLandmarks
from multiprocessing import Process, Queue

class SharedData:
    def __init__(self):
        self.latest_landmarks = None
        self.latest_rgb_image = None

# Define common constants
FRAME_INTERVAL = 1/60  # 60 FPS

def main_loop(shared_data):
    # Convert once and share
    rgb_image = cv2.cvtColor(np_mmap, cv2.COLOR_BGRA2RGB)
    shared_data.latest_rgb_image = rgb_image
    
    holistic_detector.inference(rgb_image)

    # Filtering (Note: use copy.deepcopy when filtering results)
    results = holistic_detector.results

    # Send results to solver app
    packed_results = packer.pack_holistic_landmarks_result(results)
    pose_sender.send_holistic_landmarks(packed_results)

    return True

def server_loop(shared_data):
    print("Starting server loop...")
    filtered_result_receiver = UdpServer("localhost", 9002)
    filtered_result_receiver.bind()
    
    def handle_received_data(raw_results):
        results = HolisticLandmarks()
        results.ParseFromString(raw_results)
        shared_data.latest_landmarks = results
        print("Received new landmarks")
    
    while True:
        filtered_result_receiver.receive(handle_received_data)
        time.sleep(FRAME_INTERVAL) 

def visualize_result(shared_data):
    while True:
        if shared_data.latest_landmarks is None:
            time.sleep(FRAME_INTERVAL)
            continue

        # Skip frames if processing is too slow
        if time.time() - last_process_time < FRAME_INTERVAL:
            continue

        # Process frame
        last_process_time = time.time()
        annotated_image = np.array(shared_data.latest_rgb_image, copy=True)
        
        results = shared_data.latest_landmarks
        if results is not None:
            annotated_image = visualizer.draw_all_landmarks(annotated_image, results)

        cv2.imshow('External Landmarks', cv2.flip(cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR), 1))
        
        if cv2.waitKey(1) & 0xFF == 27:
            break

if __name__ == "__main__":
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    pose_sender = HolisticPoseSender("localhost", 9001)
    pose_sender.connect()

    holistic_detector = HolisticDetector(5)

    width = 1280
    height = 720

    project_root_directory = str(Path(__file__).parent.parent.parent)
    filepath = project_root_directory + "/colorImg.dat"

    np_mmap = np.memmap(
        filepath,
        dtype='uint8',
        mode='r',
        shape=(height, width, 4),
    )

    shared_data = SharedData()
    
    # Use Process instead of Thread for CPU-intensive tasks
    Process(target=server_loop, args=(shared_data,)).start()
    Process(target=visualize_result, args=(shared_data,)).start()

    doLoop = True
    while doLoop:
        doLoop = main_loop(shared_data)
        time.sleep(FRAME_INTERVAL)  # Use common interval

    cv2.destroyAllWindows()
from network.holistic_pose_sender import HolisticPoseSender
from holistic_detector import HolisticDetector
import packer
import visualizer

import cv2
import mediapipe as mp
import numpy as np

from pathlib import Path
from filters.moving_average_filter import MovingAverage, no_process
import time
import copy

def main_loop(landmark_filter):
  # Break in key Ctrl+C pressed
  if cv2.waitKey(5) & 0xFF == 27:
    return False

  image = cv2.cvtColor(np_mmap, cv2.COLOR_BGRA2RGB)
  holistic_detector.inference(image)

  # Filtering
  results = copy.deepcopy(holistic_detector.results)
  landmark_filter['pose'].update(results.pose_landmarks)
  landmark_filter['hand'].update(results.hand_landmarks)
  results.pose_landmarks = landmark_filter['pose'].result
  results.hand_landmarks = landmark_filter['hand'].result

  # Send results to solver app
  packed_results = packer.pack_holistic_landmarks_result(results)
  pose_sender.send_holistic_landmarks(packed_results)

  # Visualize resulted landmarks
  annotated_image = image
  if results.pose_landmarks is not None:
    annotated_image = visualizer.draw_pose_landmarks_on_image(annotated_image, results.pose_landmarks)
  if results.hand_landmarks is not None:
    annotated_image = visualizer.draw_hand_landmarks_on_image(annotated_image, results.hand_landmarks)
  if results.face_results is not None:
    annotated_image = visualizer.draw_face_landmarks_on_image(annotated_image, results.face_results)
  cv2.imshow('MediaPipe Landmarks', cv2.flip(cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR), 1))
  return True

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


  filter = {
    'pose': MovingAverage(1, no_process),
    'hand': MovingAverage(1, no_process)
  }

  doLoop = True
  while doLoop:
    doLoop = main_loop(filter)
    time.sleep(1/60)

  cv2.destroyAllWindows()
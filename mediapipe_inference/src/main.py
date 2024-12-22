from holistic_pose_sender import HolisticPoseSender
from holistic_detector import HolisticDetector
import visualizer

import cv2
import mediapipe as mp
import numpy as np


if __name__ == "__main__":
  mp_drawing = mp.solutions.drawing_utils
  mp_drawing_styles = mp.solutions.drawing_styles

  pose_sender = HolisticPoseSender("localhost", 9001)
  pose_sender.connect()

  holistic_detector = HolisticDetector()

  width = 1280
  height = 720
  filepath = "../colorImg.dat"

  np_mmap = np.memmap(
      filepath,
      dtype='uint8',
      mode='r',
      shape=(height, width, 4),
  )

  while True:
      # Break in key Ctrl+C pressed
      if cv2.waitKey(5) & 0xFF == 27:
          break

      image = cv2.cvtColor(np_mmap, cv2.COLOR_BGRA2RGB)
      holistic_detector.inference(image)
      pose_sender.send_holistic_landmarks(holistic_detector.results())

      # Visualize resulted landmarks
      annotated_image = image
      if holistic_detector.results().pose_landmarks is not None:
        annotated_image = visualizer.draw_pose_landmarks_on_image(annotated_image, holistic_detector.results().pose_landmarks)
      if holistic_detector.results().hand_landmarks is not None:
        annotated_image = visualizer.draw_hand_landmarks_on_image(annotated_image, holistic_detector.results().hand_landmarks)
      if holistic_detector.results().face_results is not None:
        annotated_image = visualizer.draw_face_landmarks_on_image(annotated_image, holistic_detector.results().face_results)
      cv2.imshow('MediaPipe Landmarks', cv2.flip(cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR), 1))
  cv2.destroyAllWindows()
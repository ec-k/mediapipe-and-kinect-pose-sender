import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from unpacker import unpack
import numpy as np


def draw_pose_landmarks_on_image(rgb_image, detection_result):
  # pose_landmarks_list = unpack(detection_result.landmarks)
  pose_landmarks = list(detection_result.landmarks)
  annotated_image = np.copy(rgb_image)

  # Draw the pose landmarks.
  pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
  pose_landmarks_proto.landmark.extend([
    landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
  ])
  solutions.drawing_utils.draw_landmarks(
    annotated_image,
    pose_landmarks_proto,
    solutions.pose.POSE_CONNECTIONS,
    solutions.drawing_styles.get_default_pose_landmarks_style())
  return annotated_image

def draw_hand_landmarks_on_image(rgb_image, detection_result):
  hand_landmarks = list(detection_result.landmarks)
  annotated_image = np.copy(rgb_image)
  # Draw the hand landmarks.
  hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
  hand_landmarks_proto.landmark.extend([
    landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
  ])
  solutions.drawing_utils.draw_landmarks(
    annotated_image,
    hand_landmarks_proto,
    solutions.hands.HAND_CONNECTIONS,
    solutions.drawing_styles.get_default_hand_landmarks_style(),
    solutions.drawing_styles.get_default_hand_connections_style())
  return annotated_image

def draw_face_landmarks_on_image(rgb_image, detection_result):
  face_landmarks = list(detection_result.landmarks)
  annotated_image = np.copy(rgb_image)
  # Draw the face landmarks.
  face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
  face_landmarks_proto.landmark.extend([
    landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
  ])

  solutions.drawing_utils.draw_landmarks(
      image=annotated_image,
      landmark_list=face_landmarks_proto,
      connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
      landmark_drawing_spec=None,
      connection_drawing_spec=mp.solutions.drawing_styles
      .get_default_face_mesh_tesselation_style())
  solutions.drawing_utils.draw_landmarks(
      image=annotated_image,
      landmark_list=face_landmarks_proto,
      connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
      landmark_drawing_spec=None,
      connection_drawing_spec=mp.solutions.drawing_styles
      .get_default_face_mesh_contours_style())
  solutions.drawing_utils.draw_landmarks(
      image=annotated_image,
      landmark_list=face_landmarks_proto,
      connections=mp.solutions.face_mesh.FACEMESH_IRISES,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_iris_connections_style())

  return annotated_image

def draw_all_landmarks(rgb_image, holistic_results):
    """Draw all landmarks (pose, hands, face) on the image.
    
    Args:
        rgb_image: RGB format image
        holistic_results: HolisticLandmarks containing pose, hands and face data
    
    Returns:
        Image with all landmarks drawn
    """
    annotated_image = np.array(rgb_image, copy=True)
    
    # Draw pose landmarks
    if holistic_results.poseLandmarks is not None:
        annotated_image = draw_pose_landmarks_on_image(
            annotated_image, 
            holistic_results.poseLandmarks
        )
    
    # Draw left hand landmarks
    if holistic_results.leftHandLandmarks is not None:
        annotated_image = draw_hand_landmarks_on_image(
            annotated_image, 
            holistic_results.leftHandLandmarks
        )
    
    # Draw right hand landmarks
    if holistic_results.rightHandLandmarks is not None:
        annotated_image = draw_hand_landmarks_on_image(
            annotated_image, 
            holistic_results.rightHandLandmarks
        )
    
    # Draw face landmarks
    if holistic_results.faceResults is not None:
        annotated_image = draw_face_landmarks_on_image(
            annotated_image, 
            holistic_results.faceResults
        )
    
    return annotated_image
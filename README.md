# MediaPipe & Kinect pose sender

This is pose estimation app with MediaPipe and Kinect.
Estimate pose by Kinect Body Tracking. Estimate face and hands by MediaPipe.

# How to Use

1. Run c#\_runtime
2. Run mediapipe_inference/main.py
3. Run Solver App that uses holistic_landmarks.proto defined in this repo (mediapipe_inference/src/proto/holistic_landmarks.proto)

This app need some file for Memory Mapped Files so you may need to place some file in root of this repo directory and name it "colorImg.dat".

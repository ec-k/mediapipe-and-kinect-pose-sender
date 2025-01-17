# MediaPipe & Kinect pose sender

This is pose estimation app with MediaPipe and Kinect.
Estimate pose by Kinect Body Tracking. Estimate face and hands by MediaPipe.

# How to Use

1. Run c#\_runtime
2. Run mediapipe_inference/main.py
3. Run Solver App that uses holistic_landmarks.proto defined in this repo (mediapipe_inference/src/proto/holistic_landmarks.proto)

In first use, you need run c#\_runtime first to create a file to use in Memory Mapped File.

# Installation
- Place mediapipe models in mediapipe_inference/models
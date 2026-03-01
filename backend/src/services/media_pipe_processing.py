import os
import cv2
import numpy as np
from mediapipe.tasks.python.core.base_options import BaseOptions
from mediapipe.tasks.python.vision import PoseLandmarker, PoseLandmarkerOptions, RunningMode
from mediapipe.tasks.python.vision.pose_landmarker import PoseLandmarkerResult
import mediapipe as mp

# Build absolute path to the .task model file so it works regardless of
# where the script is run from (avoids relative path issues)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "pose_landmarker_full.task")

# Load the MediaPipe Pose Landmarker model in VIDEO mode.
# VIDEO mode processes frames sequentially with timestamps (vs IMAGE mode
# which treats each frame independently, or LIVE_STREAM for real-time webcam)
base_options = BaseOptions(model_asset_path=MODEL_PATH)
options = PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=RunningMode.VIDEO,
)
mp_pose = PoseLandmarker.create_from_options(options)


def analyze_video(video_path, frame_skip=1):
    """
    Extracts 3D joint coordinates from every Nth frame of a video.

    Args:
        video_path (str): Path to the input .mp4 video file.
        frame_skip (int): Process every Nth frame. Default 5 = 20% of frames.
                          Lower = more data but slower. Higher = faster but less detail.

    Returns:
        np.ndarray: Shape (frames, 33, 3) — frames processed × 33 body joints × (x, y, z).
                    x/y are normalized 0-1 relative to frame size. z is depth.
    """

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # Needed to compute accurate timestamps for VIDEO mode

    frame_count = 0
    joint_data = []  # Will accumulate one entry per processed frame

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # End of video or read error

        # Skip frames to speed up processing (e.g. frame_skip=5 means process frames 0, 5, 10, ...)
        if frame_count % frame_skip != 0:
            frame_count += 1
            continue

        # MediaPipe expects RGB, but OpenCV loads frames as BGR — convert here
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Compute timestamp in milliseconds — MediaPipe VIDEO mode requires
        # monotonically increasing timestamps to track pose across frames
        timestamp_ms = int((frame_count / fps) * 1000)
        results = mp_pose.detect_for_video(mp_image, timestamp_ms)

        if results.pose_landmarks:
            # results.pose_landmarks is a list of people detected.
            # [0] = first person (we assume single subject in snowboard videos)
            # Each landmark has normalized x, y, z coordinates (0.0 to 1.0)
            frame_joints = []
            for landmark in results.pose_landmarks[0]:
                frame_joints.append([landmark.x, landmark.y, landmark.z, landmark.visibility])
            joint_data.append(frame_joints)  # Add this frame's 33 joints to the dataset

        frame_count += 1

    cap.release()  # Free the video file handle

    # Returns shape: (num_frames, 33, 3)
    # This gets passed to metrics.py → extract_metrics() → then to the LLM
    return np.array(joint_data)
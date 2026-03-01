import os
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python.core.base_options import BaseOptions
from mediapipe.tasks.python.vision import PoseLandmarker, PoseLandmarkerOptions, RunningMode
from mediapipe.tasks.python.vision.pose_landmarker import PoseLandmarkerResult

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "pose_landmarker_full.task")


def analyze_video(video_path, frame_skip=5):
    """
    Extracts 3D joint coordinates from every Nth frame of a video.

    Args:
        video_path (str): Path to the input .mp4 video file.
        frame_skip (int): Process every Nth frame. Default 5 = 20% of frames.
                          Lower = more data but slower. Higher = faster but less detail.

    Returns:
        np.ndarray: Shape (frames, 33, 4) — frames processed × 33 body joints × (x, y, z, visibility).
                    x/y are normalized 0-1 relative to frame size. z is depth.
    """
    base_options = BaseOptions(model_asset_path=MODEL_PATH)
    options = PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=RunningMode.VIDEO,
    )
    mp_pose = PoseLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_count = 0
    joint_data = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_skip != 0:
            frame_count += 1
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        timestamp_ms = int((frame_count / fps) * 1000)
        results = mp_pose.detect_for_video(mp_image, timestamp_ms)

        if results.pose_landmarks:
            frame_joints = []
            for landmark in results.pose_landmarks[0]:
                frame_joints.append([landmark.x, landmark.y, landmark.z, landmark.visibility])
            joint_data.append(frame_joints)

        frame_count += 1

    cap.release()
    mp_pose.close()

    return np.array(joint_data)
import numpy as np

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
              np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = abs(radians * 180.0 / np.pi)
    if angle > 180:
        angle = 360 - angle
    return angle


def extract_metrics(joint_data):
    knee_angles = []
    hip_angles = []
    elbow_angles = []

    for frame in joint_data:
        # Knee angle (right side)
        knee_angles.append(calculate_angle(frame[24], frame[26], frame[28]))
        # Hip angle (right side)
        hip_angles.append(calculate_angle(frame[12], frame[24], frame[26]))
        # Elbow angle (right side)
        elbow_angles.append(calculate_angle(frame[12], frame[14], frame[16]))

    return {
        # Summary stats (for quick overview)
        "knee_angle_avg": float(np.mean(knee_angles)),
        "knee_angle_min": float(np.min(knee_angles)),
        "knee_angle_max": float(np.max(knee_angles)),

        "hip_angle_avg": float(np.mean(hip_angles)),
        "hip_angle_min": float(np.min(hip_angles)),

        "elbow_angle_avg": float(np.mean(elbow_angles)),

        # Per-frame timeline (so LLM can spot exactly when form breaks down)
        "frame_by_frame": [
            {
                "frame": i,
                "knee_angle": round(knee_angles[i], 2),
                "hip_angle": round(hip_angles[i], 2),
                "elbow_angle": round(elbow_angles[i], 2),
            }
            for i in range(len(knee_angles))
        ]
    }




#KYLE CALLES THIS
# from video_processor import analyze_video
# from metrics import extract_metrics

# def redwings_biometric_analysis(video_path):
#     joints = analyze_video(video_path)
#     metrics = extract_metrics(joints)
#     return metrics
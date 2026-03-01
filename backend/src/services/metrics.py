import numpy as np
from scipy.signal import savgol_filter

def calculate_angle(a, b, c):
    """
    Calculates the 3D angle (in degrees) at point B formed by the vector A→B→C.
    Uses x, y, and z coordinates so it works regardless of camera angle.

    Args:
        a, b, c: Each is a [x, y, z, visibility] landmark coordinate.
                 b is the vertex (the joint we're measuring the angle at).
                 e.g. for knee angle: a=hip, b=knee, c=ankle

    Returns:
        float: Angle in degrees (0-180), or None if any landmark has low confidence.
    """
    if len(a) > 3 and (a[3] < 0.5 or b[3] < 0.5 or c[3] < 0.5):
        return None

    a = np.array(a[:3])
    b = np.array(b[:3])
    c = np.array(c[:3])

    ba = a - b
    bc = c - b

    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    cosine = np.clip(cosine, -1.0, 1.0)

    return float(np.degrees(np.arccos(cosine)))


def calculate_distance(a, b):
    """
    Calculates true 3D Euclidean distance between two landmarks.
    Uses all 3 axes so distance is accurate regardless of camera angle.
    """
    return float(np.linalg.norm(np.array(a[:3]) - np.array(b[:3])))


def smooth_angles(angles, window=7, poly=2):
    """
    Applies Savitzky-Golay smoothing to reduce MediaPipe jitter.
    None values (low-confidence frames) are interpolated before smoothing.

    Args:
        angles: list of floats or None values
        window: smoothing window size (must be odd — larger = smoother)
        poly:   polynomial order for the filter

    Returns:
        list of smoothed floats
    """
    arr = np.array(angles, dtype=float)
    nans = np.isnan(arr)

    if nans.all():
        return angles

    indices = np.arange(len(arr))
    arr[nans] = np.interp(indices[nans], indices[~nans], arr[~nans])

    if len(arr) < window:
        return arr.tolist()

    return savgol_filter(arr, window_length=window, polyorder=poly).tolist()


def detect_phases(frame_by_frame):
    """
    Labels each frame based on body position rather than trick type.
    Skill-agnostic — works for jumps, carves, presses, spins, rails etc.

    Phase labels:
        extended         — legs straight, approach / landing / riding tall
        deep_compression — both knee and hip very bent, deep press / hard landing
        knee_compression — knees bent but hip upright, ollie prep / carve
        hip_hinge        — forward lean dominant, nose or tail press / butter
        arms_tucked      — arms pulled in tight, likely a spin or rotation
        athletic_stance  — balanced neutral riding position
        unknown          — low confidence landmarks, unreliable frame
    """
    phases = []
    for f in frame_by_frame:
        knee = f["right_knee_angle"]
        hip  = f["right_hip_angle"]
        arm  = f["arm_spread"]

        if knee is None or hip is None:
            phase = "unknown"
        elif knee > 160 and hip > 150:
            phase = "extended"
        elif knee < 90 and hip < 90:
            phase = "deep_compression"
        elif knee < 90:
            phase = "knee_compression"
        elif hip < 110:
            phase = "hip_hinge"
        elif arm is not None and arm < 0.05:
            phase = "arms_tucked"
        else:
            phase = "athletic_stance"

        phases.append({"frame": f["frame"], "phase": phase})
    return phases


def extract_metrics(joint_data):
    """
    Converts raw joint coordinate data into biomechanical metrics for LLM analysis.

    MediaPipe Pose landmark indices used:
        11 = left shoulder,  12 = right shoulder
        13 = left elbow,     14 = right elbow
        15 = left wrist,     16 = right wrist
        23 = left hip,       24 = right hip
        25 = left knee,      26 = right knee
        27 = left ankle,     28 = right ankle

    Args:
        joint_data (np.ndarray): Shape (frames, 33, 4) from analyze_video().
                                 Last dim = [x, y, z, visibility]

    Returns:
        dict: Summary stats + per-frame breakdown ready for LLM consumption.
              Returns error dict if no pose was detected.
    """
    if len(joint_data) == 0:
        return {}

    right_knee_angles  = []
    left_knee_angles   = []
    right_hip_angles   = []
    right_elbow_angles = []
    arm_spread         = []
    stance_width       = []
    center_of_mass_x   = []
    center_of_mass_y   = []

    for frame in joint_data:
        right_knee_angles.append(calculate_angle(frame[24], frame[26], frame[28]))
        left_knee_angles.append(calculate_angle(frame[23], frame[25], frame[27]))
        right_hip_angles.append(calculate_angle(frame[12], frame[24], frame[26]))
        right_elbow_angles.append(calculate_angle(frame[12], frame[14], frame[16]))

        arm_spread.append(calculate_distance(frame[15], frame[16]))
        stance_width.append(calculate_distance(frame[27], frame[28]))

        center_of_mass_x.append(float((frame[23][0] + frame[24][0]) / 2))
        center_of_mass_y.append(float((frame[23][1] + frame[24][1]) / 2))

    # Smooth all angle lists to remove MediaPipe jitter
    right_knee_angles  = smooth_angles(right_knee_angles)
    left_knee_angles   = smooth_angles(left_knee_angles)
    right_hip_angles   = smooth_angles(right_hip_angles)
    right_elbow_angles = smooth_angles(right_elbow_angles)

    # Filter physically impossible angles — < 25° are glitches
    valid_right_knee = [a for a in right_knee_angles if a is not None and a > 25]
    valid_hip        = [a for a in right_hip_angles  if a is not None and a > 25]

    # Guard against empty lists — means pose was not detected in video
    if not valid_right_knee or not valid_hip:
        return {
            "error": "Could not detect pose in video. Make sure the full body is visible in the frame.",
            "knee_angle_avg": None,
            "knee_angle_min": None,
            "knee_angle_max": None,
            "knee_symmetry_avg": None,
            "hip_angle_avg": None,
            "hip_angle_min": None,
            "elbow_angle_avg": None,
            "arm_spread_avg": None,
            "arm_spread_min": None,
            "stance_width_avg": None,
            "center_of_mass_x_avg": None,
            "center_of_mass_x_std": None,
            "knee_velocity_max": None,
            "knee_velocity_avg": None,
            "trick_phases": [],
            "frame_by_frame": [],
        }

    # Knee symmetry — left vs right difference per frame
    knee_symmetry = [
        abs(right_knee_angles[i] - left_knee_angles[i])
        if right_knee_angles[i] is not None and left_knee_angles[i] is not None
        else 0.0
        for i in range(len(right_knee_angles))
    ]

    # Knee velocity — frame-to-frame angle change, detects hard landings
    knee_velocity = [
        abs(right_knee_angles[i] - right_knee_angles[i - 1])
        if right_knee_angles[i] is not None and right_knee_angles[i - 1] is not None
        else 0.0
        for i in range(1, len(right_knee_angles))
    ]

    # Per-frame timeline for LLM temporal analysis
    frame_by_frame = [
        {
            "frame": i,
            "right_knee_angle": round(right_knee_angles[i], 2) if right_knee_angles[i] is not None else None,
            "left_knee_angle":  round(left_knee_angles[i], 2)  if left_knee_angles[i]  is not None else None,
            "knee_symmetry":    round(knee_symmetry[i], 2),
            "right_hip_angle":  round(right_hip_angles[i], 2)  if right_hip_angles[i]  is not None else None,
            "elbow_angle":      round(right_elbow_angles[i], 2) if right_elbow_angles[i] is not None else None,
            "arm_spread":       round(arm_spread[i], 3),
            "stance_width":     round(stance_width[i], 3),
            "center_of_mass_x": round(center_of_mass_x[i], 3),
        }
        for i in range(len(right_knee_angles))
    ]

    return {
        "knee_angle_avg":        float(np.mean(valid_right_knee)),
        "knee_angle_min":        float(np.min(valid_right_knee)),
        "knee_angle_max":        float(np.max(valid_right_knee)),
        "knee_symmetry_avg":     float(np.mean(knee_symmetry)),

        "hip_angle_avg":         float(np.mean(valid_hip)),
        "hip_angle_min":         float(np.min(valid_hip)),

        "elbow_angle_avg":       float(np.mean([a for a in right_elbow_angles if a is not None])),
        "arm_spread_avg":        float(np.mean(arm_spread)),
        "arm_spread_min":        float(np.min(arm_spread)),

        "stance_width_avg":      float(np.mean(stance_width)),
        "center_of_mass_x_avg":  float(np.mean(center_of_mass_x)),
        "center_of_mass_x_std":  float(np.std(center_of_mass_x)),

        "knee_velocity_max":     float(np.max(knee_velocity)),
        "knee_velocity_avg":     float(np.mean(knee_velocity)),

        "trick_phases":          detect_phases(frame_by_frame),
        "frame_by_frame":        frame_by_frame,
    }
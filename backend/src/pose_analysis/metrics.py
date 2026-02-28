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
    # Filter out low-confidence landmarks before calculating
    if len(a) > 3 and (a[3] < 0.5 or b[3] < 0.5 or c[3] < 0.5):
        return None

    a = np.array(a[:3])
    b = np.array(b[:3])
    c = np.array(c[:3])

    ba = a - b
    bc = c - b

    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    cosine = np.clip(cosine, -1.0, 1.0)
    angle = np.degrees(np.arccos(cosine))

    return float(angle)


def calculate_distance(a, b):
    """
    Calculates true 3D Euclidean distance between two landmarks.
    Using 3D (not just x,y) so distance is accurate regardless of camera angle.
    """
    return float(np.linalg.norm(np.array(a[:3]) - np.array(b[:3])))


def smooth_angles(angles, window=7, poly=2):
    """
    Applies Savitzky-Golay smoothing to reduce MediaPipe jitter.
    Replaces None values with interpolated estimates before smoothing.

    Args:
        angles: list of floats or None values
        window: smoothing window (must be odd, larger = smoother)
        poly: polynomial order

    Returns:
        list of smoothed floats
    """
    # Replace None with linear interpolation
    arr = np.array(angles, dtype=float)
    nans = np.isnan(arr)
    if nans.all():
        return angles
    indices = np.arange(len(arr))
    arr[nans] = np.interp(indices[nans], indices[~nans], arr[~nans])

    # Need at least window_length points to smooth
    if len(arr) < window:
        return arr.tolist()

    return savgol_filter(arr, window_length=window, polyorder=poly).tolist()


def detect_phases(frame_by_frame):
    """
    Labels each frame based on body position rather than trick type.
    Works for any snowboarding skill — carves, jumps, presses, spins, rails etc.

    Phases:
        extended         — standing tall, approach/landing/riding
        deep_compression — very bent, hard landing/deep carve/press
        knee_compression — knees bent, ollie prep/press/carve
        hip_hinge        — forward lean, buttering/nose/tail press
        arms_tucked      — arms in, spin/rotation
        athletic_stance  — normal riding position
    """
    phases = []
    for f in frame_by_frame:
        knee = f["right_knee_angle"]
        hip = f["right_hip_angle"]
        arm = f["arm_spread"]

        if knee > 160 and hip > 150:
            phase = "extended"
        elif knee < 90 and hip < 90:
            phase = "deep_compression"
        elif knee < 90:
            phase = "knee_compression"
        elif hip < 110:
            phase = "hip_hinge"
        elif arm < 0.05:
            phase = "arms_tucked"
        else:
            phase = "athletic_stance"

        phases.append({"frame": f["frame"], "phase": phase})
    return phases


def extract_metrics(joint_data):
    """
    Converts raw joint coordinate data into biomechanical metrics for LLM analysis.

    MediaPipe Pose landmark indices:
        11 = left shoulder,  12 = right shoulder
        13 = left elbow,     14 = right elbow
        15 = left wrist,     16 = right wrist
        23 = left hip,       24 = right hip
        25 = left knee,      26 = right knee
        27 = left ankle,     28 = right ankle

    Args:
        joint_data (np.ndarray): Shape (frames, 33, 4) from analyze_video().
                                 4 = [x, y, z, visibility]

    Returns:
        dict: Summary stats + per-frame breakdown for LLM consumption.
    """
    if len(joint_data) == 0:
        return {}

    # --- Per-frame metric lists (None = low confidence frame) ---
    right_knee_angles = []
    left_knee_angles = []
    right_hip_angles = []
    right_elbow_angles = []
    arm_spread = []
    stance_width = []
    center_of_mass_x = []
    center_of_mass_y = []

    for frame in joint_data:
        right_knee_angles.append(calculate_angle(frame[24], frame[26], frame[28]))
        left_knee_angles.append(calculate_angle(frame[23], frame[25], frame[27]))
        right_hip_angles.append(calculate_angle(frame[12], frame[24], frame[26]))
        right_elbow_angles.append(calculate_angle(frame[12], frame[14], frame[16]))

        # 3D distances — accurate regardless of camera angle
        arm_spread.append(calculate_distance(frame[15], frame[16]))
        stance_width.append(calculate_distance(frame[27], frame[28]))

        # Center of mass proxy: midpoint between hips
        hip_mid_x = (frame[23][0] + frame[24][0]) / 2
        hip_mid_y = (frame[23][1] + frame[24][1]) / 2
        center_of_mass_x.append(float(hip_mid_x))
        center_of_mass_y.append(float(hip_mid_y))

    # --- Smooth all angle lists to remove MediaPipe jitter ---
    # This stabilizes phase detection and reduces false flags significantly
    right_knee_angles = smooth_angles(right_knee_angles)
    left_knee_angles  = smooth_angles(left_knee_angles)
    right_hip_angles  = smooth_angles(right_hip_angles)
    right_elbow_angles = smooth_angles(right_elbow_angles)

    # --- Filter out physically impossible angles (< 25° are glitches) ---
    valid_right_knee = [a for a in right_knee_angles if a > 25]
    valid_hip        = [a for a in right_hip_angles  if a > 25]

    # --- Knee symmetry ---
    # Side-view: expect high values naturally. Flag > 60° only.
    # Front-view: flag > 20°.
    knee_symmetry = [abs(right_knee_angles[i] - left_knee_angles[i])
                     for i in range(len(right_knee_angles))]

    # --- Joint velocity: angle change frame-to-frame ---
    # High = explosive/sudden movement, useful for flagging hard landings
    knee_velocity = [abs(right_knee_angles[i] - right_knee_angles[i-1])
                     for i in range(1, len(right_knee_angles))]

    # --- Build per-frame timeline ---
    frame_by_frame = [
        {
            "frame": i,
            "right_knee_angle": round(right_knee_angles[i], 2),
            "left_knee_angle": round(left_knee_angles[i], 2),
            "knee_symmetry": round(knee_symmetry[i], 2),
            "right_hip_angle": round(right_hip_angles[i], 2),
            "elbow_angle": round(right_elbow_angles[i], 2),
            "arm_spread": round(arm_spread[i], 3),
            "stance_width": round(stance_width[i], 3),
            "center_of_mass_x": round(center_of_mass_x[i], 3),
        }
        for i in range(len(right_knee_angles))
    ]

    return {
        # --- Knee metrics ---
        "knee_angle_avg": float(np.mean(valid_right_knee)),
        "knee_angle_min": float(np.min(valid_right_knee)),   # Deepest bend (landing impact)
        "knee_angle_max": float(np.max(valid_right_knee)),   # Most extended (in-air)
        "knee_symmetry_avg": float(np.mean(knee_symmetry)),  # Side-view: flag > 60°, front-view: flag > 20°

        # --- Hip metrics ---
        "hip_angle_avg": float(np.mean(valid_hip)),
        "hip_angle_min": float(np.min(valid_hip)),           # Most forward lean

        # --- Arm/balance metrics ---
        "elbow_angle_avg": float(np.mean(right_elbow_angles)),
        "arm_spread_avg": float(np.mean(arm_spread)),        # Higher = arms out for balance
        "arm_spread_min": float(np.min(arm_spread)),         # Near 0 = arms tucked (likely spinning)

        # --- Stance & balance ---
        "stance_width_avg": float(np.mean(stance_width)),
        "center_of_mass_x_avg": float(np.mean(center_of_mass_x)),  # ~0.5 = centered
        "center_of_mass_x_std": float(np.std(center_of_mass_x)),   # High = unstable side-to-side

        # --- Joint velocity ---
        "knee_velocity_max": float(np.max(knee_velocity)),   # Hardest landing moment
        "knee_velocity_avg": float(np.mean(knee_velocity)),

        # --- Trick phase segmentation ---
        "trick_phases": detect_phases(frame_by_frame),

        # --- Full per-frame timeline for LLM ---
        "frame_by_frame": frame_by_frame,
    }
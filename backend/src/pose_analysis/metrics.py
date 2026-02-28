import numpy as np

def calculate_angle(a, b, c):
    """
    Calculates the angle (in degrees) at point B formed by the vector A→B→C.

    Args:
        a, b, c: Each is a [x, y, z] landmark coordinate.
                 b is the vertex (the joint we're measuring the angle at).
                 e.g. for knee angle: a=hip, b=knee, c=ankle

    Returns:
        float: Angle in degrees (0-180).
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
              np.arctan2(a[1]-b[1], a[0]-b[0])

    angle = abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


def calculate_distance(a, b):
    """
    Calculates Euclidean distance between two landmarks (x, y only).
    Used for arm spread and balance width calculations.
    """
    return float(np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2))


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
        joint_data (np.ndarray): Shape (frames, 33, 3) from analyze_video().

    Returns:
        dict: Summary stats + per-frame breakdown for LLM consumption.
    """
    if len(joint_data) == 0:
        return {}

    # --- Per-frame metric lists ---
    right_knee_angles = []
    left_knee_angles = []
    right_hip_angles = []
    left_hip_angles = []
    right_elbow_angles = []
    shoulder_angles = []   # Shoulder tilt — detects upper/lower body counter-rotation
    arm_spread = []        # Distance between wrists — wide arms = better balance
    stance_width = []      # Distance between ankles — base of support
    center_of_mass_x = []  # Lateral balance proxy (left/right weight shift)
    center_of_mass_y = []  # Vertical balance proxy (up/down position)

    for frame in joint_data:
        # --- Both sides for symmetry comparison ---
        right_knee_angles.append(calculate_angle(frame[24], frame[26], frame[28]))
        left_knee_angles.append(calculate_angle(frame[23], frame[25], frame[27]))

        right_hip_angles.append(calculate_angle(frame[12], frame[24], frame[26]))
        left_hip_angles.append(calculate_angle(frame[11], frame[23], frame[25]))

        right_elbow_angles.append(calculate_angle(frame[12], frame[14], frame[16]))

        # Shoulder tilt: angle between left and right shoulder relative to horizontal
        # Close to 180° = level shoulders, lower = significant tilt/rotation
        shoulder_angles.append(calculate_angle(frame[11], frame[12], [frame[12][0]+0.1, frame[12][1], frame[12][2]]))

        # Arm spread: wider = better balance, very narrow = arms tucked (spin)
        arm_spread.append(calculate_distance(frame[15], frame[16]))

        # Stance width: distance between ankles
        stance_width.append(calculate_distance(frame[27], frame[28]))

        # Center of mass proxy: midpoint between hips
        # x tells us left/right lean, y tells us crouch height
        hip_mid_x = (frame[23][0] + frame[24][0]) / 2
        hip_mid_y = (frame[23][1] + frame[24][1]) / 2
        center_of_mass_x.append(float(hip_mid_x))
        center_of_mass_y.append(float(hip_mid_y))

    # --- Knee symmetry: difference between left and right knee each frame ---
    # Large differences indicate favoring one side (injury risk)
    knee_symmetry = [abs(right_knee_angles[i] - left_knee_angles[i]) for i in range(len(right_knee_angles))]

    # --- Joint velocity: how fast knee angle changes frame to frame ---
    # High velocity = explosive/sudden movement, useful for flagging hard landings
    knee_velocity = [abs(right_knee_angles[i] - right_knee_angles[i-1]) for i in range(1, len(right_knee_angles))]

    return {
        # --- Knee metrics ---
        "knee_angle_avg": float(np.mean(right_knee_angles)),
        "knee_angle_min": float(np.min(right_knee_angles)),   # Deepest bend (landing impact)
        "knee_angle_max": float(np.max(right_knee_angles)),   # Most extended (in-air)
        "knee_symmetry_avg": float(np.mean(knee_symmetry)),   # Avg left/right difference (>20° = concerning)

        # --- Hip metrics ---
        "hip_angle_avg": float(np.mean(right_hip_angles)),
        "hip_angle_min": float(np.min(right_hip_angles)),

        # --- Arm/balance metrics ---
        "elbow_angle_avg": float(np.mean(right_elbow_angles)),
        "arm_spread_avg": float(np.mean(arm_spread)),          # Higher = arms out for balance
        "arm_spread_min": float(np.min(arm_spread)),           # Near 0 = arms tucked (likely spinning)

        # --- Stance & balance ---
        "stance_width_avg": float(np.mean(stance_width)),
        "center_of_mass_x_avg": float(np.mean(center_of_mass_x)),  # ~0.5 = centered
        "center_of_mass_x_std": float(np.std(center_of_mass_x)),   # High std = unstable side-to-side

        # --- Joint velocity (explosiveness/impact detection) ---
        "knee_velocity_max": float(np.max(knee_velocity)),     # Highest = hardest landing moment
        "knee_velocity_avg": float(np.mean(knee_velocity)),

        # --- Per-frame timeline for LLM ---
        "frame_by_frame": [
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
    }
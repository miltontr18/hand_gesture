import math

def vec(a, b):
    return (b.x - a.x, b.y - a.y, b.z - a.z)

def angle_deg(v1, v2):
    dot = v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]
    n1 = math.sqrt(sum(x*x for x in v1))
    n2 = math.sqrt(sum(x*x for x in v2))
    if n1 < 1e-9 or n2 < 1e-9:
        return 0.0
    c = max(-1.0, min(1.0, dot/(n1*n2)))
    return math.degrees(math.acos(c))

def finger_extended(lm, mcp_i, pip_i, dip_i, tip_i, thresh=160):
    v1 = vec(lm[pip_i], lm[mcp_i])
    v2 = vec(lm[pip_i], lm[dip_i])
    ang_pip = angle_deg(v1, v2)

    v3 = vec(lm[dip_i], lm[pip_i])
    v4 = vec(lm[dip_i], lm[tip_i])
    ang_dip = angle_deg(v3, v4)

    return 1 if (ang_pip > thresh and ang_dip > thresh) else 0

def thumb_extended(lm, thresh=150):
    v1 = vec(lm[3], lm[2])
    v2 = vec(lm[3], lm[4])
    ang_ip = angle_deg(v1, v2)

    v3 = vec(lm[2], lm[1])
    v4 = vec(lm[2], lm[3])
    ang_mcp = angle_deg(v3, v4)

    return 1 if (ang_ip > thresh and ang_mcp > thresh) else 0

def get_finger_states(hand_landmarks):
    lm = hand_landmarks.landmark
    return [
        thumb_extended(lm),
        finger_extended(lm, 5, 6, 7, 8),
        finger_extended(lm, 9, 10, 11, 12),
        finger_extended(lm, 13, 14, 15, 16),
        finger_extended(lm, 17, 18, 19, 20),
    ]

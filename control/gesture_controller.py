import cv2, time
import mediapipe as mp
from network.esp32_socket import safe_send
from vision.hand_utils import get_finger_states
from vision.gesture_detection import detect_gesture, arm_pose
from config import settings

def run(sock, cap):
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    prev_cmd = 'S'
    last_sent = time.time()
    safe_send(sock, 'S')

    candidate_cmd = prev_cmd
    committed_cmd = prev_cmd
    candidate_since = time.time()
    armed = False
    combo_start, last_toggle = None, 0

    with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.75, min_tracking_confidence=0.85) as hands:
        while True:
            ret, img = cap.read()
            if not ret:
                continue

            img = cv2.flip(img, 1)
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            hand_infos = []
            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_lms, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    label = handedness.classification[0].label
                    mp_drawing.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
                    f = get_finger_states(hand_lms)
                    hand_infos.append({"label": label, "f": f, "lm": hand_lms})

            # --- ARM/DISARM detection ---
            if len(hand_infos) == 2:
                both = arm_pose(hand_infos[0]["f"]) and arm_pose(hand_infos[1]["f"])
                if both:
                    combo_start = combo_start or time.time()
                    held = (time.time() - combo_start) >= settings.HOLD_TIME
                    can_toggle = (time.time() - last_toggle) >= settings.DEBOUNCE
                    if held and can_toggle:
                        armed = not armed
                        last_toggle = time.time()
                        combo_start = None
                        safe_send(sock, 'A' if armed else 'D')
                        committed_cmd = candidate_cmd = 'S'
                        candidate_since = time.time()
                else:
                    combo_start = None

            # --- Gesture detection (right hand) ---
            command, gesture_name = 'S', "NO RIGHT HAND"
            for h in hand_infos:
                if h["label"] == "Right":
                    command, gesture_name = detect_gesture(h["f"])
                    break
            if not armed:
                command = 'S'
                if gesture_name != "NO RIGHT HAND":
                    gesture_name = "DISARMED"

            # --- Stability filter ---
            now = time.time()
            if command != candidate_cmd:
                candidate_cmd, candidate_since = command, now
            if (now - candidate_since) >= settings.STABLE_TIME:
                committed_cmd = candidate_cmd

            if committed_cmd != prev_cmd and (now - last_sent > settings.COOLDOWN):
                safe_send(sock, committed_cmd)
                prev_cmd, last_sent = committed_cmd, now

            # --- Display overlay ---
            status = "ARMED" if armed else "DISARMED"
            cv2.putText(img, f"Status: {status}", (20, 40), cv2.FONT_HERSHEY_DUPLEX, 0.9,
                        (0,255,0) if armed else (0,0,255), 2)
            cv2.putText(img, f"Right Hand: {gesture_name}", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

            cv2.imshow("Hand Gesture Control", cv2.resize(img, (640, 360)))
            if cv2.waitKey(1) & 0xFF in (ord('q'), 27):
                break

    cap.release()
    sock.close()
    cv2.destroyAllWindows()

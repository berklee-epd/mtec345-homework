import threading
import time
import tkinter as tk
from tkinter import ttk

import cv2
from mediapipe import Image, ImageFormat
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from pythonosc.udp_client import SimpleUDPClient

# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────

CAMERA_INDEX = 0
SEND_FPS = 30

MAX_HANDS = 2
MAX_FACES = 1
MAX_POSES = 8

HAND_MODEL_PATH = "hand_landmarker.task"
FACE_MODEL_PATH = "face_landmarker.task"
POSE_MODEL_PATH = "pose_landmarker.task"

FACE_KEY_INDICES = [
    7, 33, 133, 144, 145, 153, 154, 155, 157, 158, 159, 160, 161, 163, 173, 246,
    249, 263, 362, 373, 374, 380, 381, 382, 384, 385, 386, 387, 388, 390, 398, 466,
    46, 52, 53, 55, 63, 65, 66, 70, 105, 107,
    276, 282, 283, 285, 293, 295, 296, 300, 334, 336,
    469, 470, 471, 472,
    474, 475, 476, 477,
    0, 13, 14, 17, 37, 39, 40, 61, 78, 80, 81, 82, 84, 87, 88, 91, 95,
    146, 178, 181, 185, 191, 267, 269, 270, 291, 308, 310, 311, 312, 314,
    317, 318, 321, 324, 375, 402, 405, 409, 415,
    10, 21, 54, 58, 67, 93, 103, 109, 127, 132, 136, 148, 149, 150, 152,
    162, 172, 176, 234, 251, 284, 288, 297, 323, 332, 338, 356, 361, 365,
    377, 378, 379, 389, 397, 400, 454,
]

# ─────────────────────────────────────────────────────────────────────────────
# Shared state
# ─────────────────────────────────────────────────────────────────────────────

state_lock = threading.Lock()
osc_host = "127.0.0.1"
osc_port = 9000
camera_index = 0
running = True

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def landmarks_to_floats(landmarks, indices=None):
    values = []
    if indices is None:
        for lm in landmarks:
            values.extend([float(lm.x), float(lm.y), float(lm.z)])
    else:
        for i in indices:
            lm = landmarks[i]
            values.extend([float(lm.x), float(lm.y), float(lm.z)])
    return values

def get_client():
    with state_lock:
        return SimpleUDPClient(osc_host, osc_port)

def set_status(text):
    status_var.set(text)

def probe_cameras(max_index=10):
    available = []
    for i in range(max_index + 1):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available.append(i)
        cap.release()
    return available

# ─────────────────────────────────────────────────────────────────────────────
# GUI
# ─────────────────────────────────────────────────────────────────────────────

def apply_settings():
    global osc_host, osc_port, camera_index
    try:
        new_host = host_var.get().strip()
        new_port = int(port_var.get().strip())
        new_camera = int(camera_var.get().strip())
        if not new_host:
            raise ValueError("Host cannot be empty")
        with state_lock:
            osc_host = new_host
            osc_port = new_port
            camera_index = new_camera
        set_status(f"Sending to {new_host}:{new_port} | Camera {new_camera}")
    except Exception as ex:
        set_status(f"Invalid settings: {ex}")

def refresh_cameras():
    cams = probe_cameras(10)
    camera_choices.set(", ".join(map(str, cams)) if cams else "No cameras found")
    if cams and camera_var.get().strip() == "":
        camera_var.set(str(cams[0]))

def stop_app():
    global running
    running = False
    try:
        root.destroy()
    except Exception:
        pass

# ─────────────────────────────────────────────────────────────────────────────
# MediaPipe Tasks init
# ─────────────────────────────────────────────────────────────────────────────

def load_landmarkers():
    hand_base = python.BaseOptions(model_asset_path=HAND_MODEL_PATH)
    face_base = python.BaseOptions(model_asset_path=FACE_MODEL_PATH)
    pose_base = python.BaseOptions(model_asset_path=POSE_MODEL_PATH)

    hand_options = vision.HandLandmarkerOptions(
        base_options=hand_base,
        running_mode=vision.RunningMode.VIDEO,
        num_hands=MAX_HANDS,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    face_options = vision.FaceLandmarkerOptions(
        base_options=face_base,
        running_mode=vision.RunningMode.VIDEO,
        num_faces=MAX_FACES,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    pose_options = vision.PoseLandmarkerOptions(
        base_options=pose_base,
        running_mode=vision.RunningMode.VIDEO,
        num_poses=MAX_POSES,
        min_pose_detection_confidence=0.5,
        min_pose_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    return (
        vision.HandLandmarker.create_from_options(hand_options),
        vision.FaceLandmarker.create_from_options(face_options),
        vision.PoseLandmarker.create_from_options(pose_options),
    )

# ─────────────────────────────────────────────────────────────────────────────
# Main worker
# ─────────────────────────────────────────────────────────────────────────────

def worker():
    global running

    set_status("Loading camera…")

    while running:
        with state_lock:
            current_camera = camera_index

        cap = cv2.VideoCapture(current_camera)
        if cap.isOpened():
            break

        set_status(f"Waiting for camera {current_camera}…")
        time.sleep(0.5)

    if not running:
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    try:
        hand_landmarker, face_landmarker, pose_landmarker = load_landmarkers()
    except Exception as ex:
        set_status(f"Failed to load MediaPipe models: {ex}")
        running = False
        cap.release()
        return

    set_status("Ready")
    send_interval = 1.0 / SEND_FPS
    last_sent_at = 0.0

    try:
        while running:
            with state_lock:
                desired_camera = camera_index

            if desired_camera != current_camera:
                cap.release()
                current_camera = desired_camera
                set_status(f"Switching to camera {current_camera}…")
                cap = cv2.VideoCapture(current_camera)
                if not cap.isOpened():
                    set_status(f"Waiting for camera {current_camera}…")
                    while running and not cap.isOpened():
                        time.sleep(0.5)
                        cap.release()
                        cap = cv2.VideoCapture(current_camera)
                    if not running:
                        break
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                set_status(f"Ready (camera {current_camera})")

            ok, frame = cap.read()
            if not ok:
                time.sleep(0.1)
                continue

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = Image(image_format=ImageFormat.SRGB, data=rgb)
            now_ms = int(time.time() * 1000)

            hand_result = hand_landmarker.detect_for_video(mp_image, now_ms)
            face_result = face_landmarker.detect_for_video(mp_image, now_ms)
            pose_result = pose_landmarker.detect_for_video(mp_image, now_ms)

            should_send = (time.time() - last_sent_at) >= send_interval
            if should_send:
                last_sent_at = time.time()
                client = get_client()

                if hand_result and hand_result.landmarks:
                    for idx, hand_landmarks in enumerate(hand_result.landmarks[:MAX_HANDS]):
                        client.send_message(f"/hand/{idx}", landmarks_to_floats(hand_landmarks))

                if face_result and face_result.face_landmarks:
                    face_landmarks = face_result.face_landmarks[0]
                    client.send_message("/face", landmarks_to_floats(face_landmarks, FACE_KEY_INDICES))

                if pose_result and pose_result.landmarks:
                    for idx, pose_landmarks in enumerate(pose_result.landmarks[:MAX_POSES]):
                        client.send_message(f"/pose/{idx}", landmarks_to_floats(pose_landmarks))

            cv2.putText(
                frame,
                f"OSC -> {osc_host}:{osc_port} | Camera {current_camera}",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame,
                "Q to quit",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )

            cv2.imshow("Local OSC Tracker", frame)
            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                running = False
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

# ─────────────────────────────────────────────────────────────────────────────
# GUI bootstrap
# ─────────────────────────────────────────────────────────────────────────────

root = tk.Tk()
root.title("Local OSC Tracker")

main = ttk.Frame(root, padding=12)
main.grid(sticky="nsew")

ttk.Label(main, text="OSC Host").grid(row=0, column=0, sticky="w")
host_var = tk.StringVar(value=osc_host)
ttk.Entry(main, textvariable=host_var, width=24).grid(row=0, column=1, sticky="ew", padx=(8, 0))

ttk.Label(main, text="OSC Port").grid(row=1, column=0, sticky="w", pady=(8, 0))
port_var = tk.StringVar(value=str(osc_port))
ttk.Entry(main, textvariable=port_var, width=24).grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(8, 0))

ttk.Label(main, text="Camera Index").grid(row=2, column=0, sticky="w", pady=(8, 0))
camera_var = tk.StringVar(value=str(camera_index))
ttk.Entry(main, textvariable=camera_var, width=24).grid(row=2, column=1, sticky="ew", padx=(8, 0), pady=(8, 0))

ttk.Button(main, text="Apply", command=apply_settings).grid(row=3, column=0, pady=(12, 0), sticky="ew")
ttk.Button(main, text="Refresh Cameras", command=refresh_cameras).grid(row=3, column=1, pady=(12, 0), sticky="ew", padx=(8, 0))

status_var = tk.StringVar(value=f"Sending to {osc_host}:{osc_port}")
ttk.Label(main, textvariable=status_var).grid(row=4, column=0, columnspan=2, sticky="w", pady=(12, 0))

camera_choices = tk.StringVar(value="")
ttk.Label(main, textvariable=camera_choices).grid(row=5, column=0, columnspan=2, sticky="w", pady=(8, 0))

ttk.Button(main, text="Quit", command=stop_app).grid(row=6, column=0, columnspan=2, pady=(12, 0), sticky="ew")

main.columnconfigure(1, weight=1)
root.protocol("WM_DELETE_WINDOW", stop_app)

refresh_cameras()
threading.Thread(target=worker, daemon=True).start()
root.mainloop()
running = False
#!/usr/bin/env python3
"""
Trackpad -> OSC -> Wekinator
Install deps: pip3 install python-osc pyobjc-framework-Quartz
Run: python3 trackpad_osc.py
"""

import time
import math
from pythonosc import udp_client

# Wekinator settings
WEKINATOR_IP = "127.0.0.1"
WEKINATOR_PORT = 6448

# OSC sender client
client = udp_client.SimpleUDPClient(WEKINATOR_IP, WEKINATOR_PORT)

# State tracking
prev_x = 0
prev_y = 0
prev_time = time.time()
still_start = time.time()
speed_history = []

try:
    from Quartz import (
        CGEventTapCreate,
        CGEventGetLocation,
        kCGEventMouseMoved,
        kCGEventLeftMouseDragged,
        kCGSessionEventTap,
        kCGHeadInsertEventTap,
        kCGEventTapOptionDefault,
        CFMachPortCreateRunLoopSource,
        CFRunLoopGetCurrent,
        CFRunLoopAddSource,
        kCFRunLoopCommonModes,
        CFRunLoopRun,
        CGEventGetIntegerValueField,
        kCGMouseEventPressure,
        kCGEventLeftMouseDown,
    )
    USE_QUARTZ = True
except ImportError:
    USE_QUARTZ = False
    print("Quartz not installed, using simple mode (mouse position only).")
    print("Install full version: pip3 install pyobjc-framework-Quartz")


def compute_features(x, y, pressure, clicked):
    global prev_x, prev_y, prev_time, still_start, speed_history

    now = time.time()
    dt = max(now - prev_time, 0.001)

    # Speed
    dx = x - prev_x
    dy = y - prev_y
    speed = math.sqrt(dx * dx + dy * dy) / dt

    # Smoothed speed (last 10 frames)
    speed_history.append(speed)
    if len(speed_history) > 10:
        speed_history.pop(0)
    smooth_speed = sum(speed_history) / len(speed_history)

    # Stillness time
    if speed > 5:
        still_start = now
    stillness = min((now - still_start) / 5.0, 1.0)  # 0-1 within 5 seconds

    # Normalize
    norm_x = min(max(x / 1920.0, 0), 1)
    norm_y = min(max(y / 1080.0, 0), 1)
    norm_speed = min(smooth_speed / 2000.0, 1)
    norm_pressure = float(pressure)
    norm_click = float(clicked)

    prev_x = x
    prev_y = y
    prev_time = now

    return [norm_x, norm_y, norm_speed, stillness, norm_pressure, norm_click]


def send_to_wekinator(features):
    client.send_message("/wek/inputs", features)
    print(
        f"Sent: x={features[0]:.2f} y={features[1]:.2f} "
        f"speed={features[2]:.2f} still={features[3]:.2f} "
        f"pressure={features[4]:.2f} click={features[5]:.0f}"
    )


if USE_QUARTZ:
    def callback(proxy, event_type, event, refcon):
        loc = CGEventGetLocation(event)
        x, y = loc.x, loc.y
        pressure = CGEventGetIntegerValueField(event, kCGMouseEventPressure) / 255.0
        clicked = 1.0 if event_type == kCGEventLeftMouseDown else 0.0
        features = compute_features(x, y, pressure, clicked)
        send_to_wekinator(features)
        return event


    print("Trackpad listener started -> Wekinator (port 6448)")
    print("Move the trackpad to send data, Ctrl+C to stop.\n")

    mask = (
        (1 << kCGEventMouseMoved)
        | (1 << kCGEventLeftMouseDragged)
        | (1 << kCGEventLeftMouseDown)
    )
    tap = CGEventTapCreate(
        kCGSessionEventTap,
        kCGHeadInsertEventTap,
        kCGEventTapOptionDefault,
        mask,
        callback,
        None,
    )

    if tap is None:
        print("Accessibility permission required.")
        print("System Settings -> Privacy & Security -> Accessibility -> add Terminal or Python")
    else:
        source = CFMachPortCreateRunLoopSource(None, tap, 0)
        CFRunLoopAddSource(CFRunLoopGetCurrent(), source, kCFRunLoopCommonModes)
        CFRunLoopRun()

else:
    # Simple mode: mouse position polling
    import subprocess

    print("Simple mode started -> Wekinator (port 6448)")
    print("Move the mouse/trackpad to send data, Ctrl+C to stop.\n")

    while True:
        try:
            # Use AppleScript to read mouse position
            result = subprocess.run(
                [
                    "osascript",
                    "-e",
                    'tell application "System Events" to get the position of the mouse cursor',
                ],
                capture_output=True,
                text=True,
                timeout=0.1,
            )
            if result.returncode == 0:
                parts = result.stdout.strip().split(", ")
                if len(parts) == 2:
                    x, y = float(parts[0]), float(parts[1])
                    features = compute_features(x, y, 0, 0)
                    send_to_wekinator(features)
        except Exception:
            pass
        time.sleep(0.05)  # 20 fps

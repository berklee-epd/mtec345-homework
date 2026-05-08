#!/usr/bin/env python3
"""
Listen to Wekinator OSC output and play state sounds.

Install dependencies:
  pip3 install python-osc pygame

Run:
  python3 play_sounds.py
"""

from __future__ import annotations

import time
from pathlib import Path

import pygame
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

OSC_IP = "0.0.0.0"
OSC_PORT = 12000
OSC_ADDRESS = "/wek/outputs"
MIN_CHANGE_INTERVAL_SECONDS = 15.0
GIVEUP_CHANGE_INTERVAL_SECONDS = 3.0

STATE_TO_SOUND = {
    1: ("CALM", "calm.mp3"),
    2: ("FOCUSED", "foucs.wav"),
    3: ("GIVING-UP", "giveup.wav"),
    4: ("SLIGHTLY-ANGRY", None),
    5: ("ANGRY", "angry.mp3"),
}

SCRIPT_DIR = Path(__file__).resolve().parent
last_state: int | None = None
audio_ready = False
last_change_time = 0.0


def ensure_audio_ready() -> bool:
    global audio_ready
    if audio_ready:
        return True

    try:
        pygame.mixer.init()
        audio_ready = True
        print("Audio engine ready.")
    except pygame.error as exc:
        # Do not crash the OSC listener if audio device is temporarily unavailable.
        print(f"[WARN] Audio init failed: {exc}")
        audio_ready = False

    return audio_ready


def play_sound(filename: str | None) -> None:
    if filename is None:
        return

    sound_path = SCRIPT_DIR / filename
    if not sound_path.exists():
        print(f"[WARN] Sound file not found: {sound_path}")
        return

    if not ensure_audio_ready():
        return

    try:
        pygame.mixer.music.load(str(sound_path))
        pygame.mixer.music.play()
    except pygame.error as exc:
        print(f"[ERROR] Failed to play '{filename}': {exc}")


def handle_wekinator_output(address: str, *args: float) -> None:
    del address
    global last_state, last_change_time

    if not args:
        return

    try:
        state = int(round(float(args[0])))
    except (TypeError, ValueError):
        print(f"[WARN] Invalid OSC payload: {args}")
        return

    if state not in STATE_TO_SOUND:
        print(f"[WARN] Unknown state {state}; expected 1-5")
        return

    # Only react when state changes.
    if state == last_state:
        return

    now = time.time()
    # Give GIVING-UP a faster response than other states.
    min_interval = (
        GIVEUP_CHANGE_INTERVAL_SECONDS if state == 3 else MIN_CHANGE_INTERVAL_SECONDS
    )
    if now - last_change_time < min_interval:
        return

    state_name, sound_file = STATE_TO_SOUND[state]
    print(f"State changed -> {state_name}")
    if sound_file is None:
        print("No sound configured for this state.")
    play_sound(sound_file)

    last_state = state
    last_change_time = now


def main() -> None:
    ensure_audio_ready()

    dispatcher = Dispatcher()
    dispatcher.map(OSC_ADDRESS, handle_wekinator_output)

    server = BlockingOSCUDPServer((OSC_IP, OSC_PORT), dispatcher)
    print(f"Listening for OSC on {OSC_IP}:{OSC_PORT} at '{OSC_ADDRESS}'")
    print("Waiting for state changes from Wekinator...")
    server.serve_forever()


if __name__ == "__main__":
    main()

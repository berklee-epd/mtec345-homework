# MediaPipe → OSC

Browser-based hand/face landmark detection (via MediaPipe) that streams
landmark data to a Node.js server, which forwards it as OSC UDP messages.

## Quick Start

```bash
npm install
npm run dev
```

Open http://localhost:5173 in a browser with webcam access (Vite’s default; if that port is busy, use the URL printed in the terminal).

## Architecture

```
Browser (Vite dev server :5173)
  └─ webcam → @mediapipe/tasks-vision (WASM)
  └─ landmarks → WebSocket (/ws) → Node server (:3001)
                                      └─ OSC UDP → configurable host:port
```

## OSC Messages

Sent as separate UDP messages at ~30fps (throttled on the client):

| Address   | Args                                                                                                                 |
| --------- | -------------------------------------------------------------------------------------------------------------------- |
| `/hand/0` | 63 floats: 21 landmarks × `x y z` (normalized image coords; see MediaPipe hand model)                                |
| `/hand/1` | Same layout for the second detected hand (zeros if absent)                                                           |
| `/face`   | 408 floats: 136 key landmark indices × `x y z` (subset of the 478-point face mesh; see `shared/face-key-indices.ts`) |

## UI Controls

- **Hand / Face** — enable either or both landmark tasks
- **OSC Host / Port** — where to send OSC (default: `127.0.0.1:9000`)

## Production Build

```bash
npm run build   # builds client to client/dist, compiles server
npm run start   # runs the server (serves client/dist at :3001)
```

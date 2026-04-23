import {
  FilesetResolver,
  HandLandmarker,
  PoseLandmarker,
  FaceLandmarker,
  DrawingUtils,
  type HandLandmarkerResult,
  type FaceLandmarkerResult,
  type PoseLandmarkerResult,
} from "@mediapipe/tasks-vision";
import type { ToServer, ToClient } from "../../shared/types.js";
import { FACE_KEY_INDICES, FACE_KEY_INDEX_SET } from "../../shared/face-key-indices.js";

// ─── DOM ─────────────────────────────────────────────────────────────────────

const video      = document.getElementById("video")     as HTMLVideoElement;
const canvas     = document.getElementById("canvas")    as HTMLCanvasElement;
const ctx        = canvas.getContext("2d")!;
const statusEl  = document.getElementById("status")!;
const dbgHand0  = document.getElementById("dbg-hand0")!;
const dbgHand1  = document.getElementById("dbg-hand1")!;
const dbgFace   = document.getElementById("dbg-face")!;
const dbgPose   = document.getElementById("dbg-pose")!;
const chkHand    = document.getElementById("chk-hand")  as HTMLInputElement;
const chkFace    = document.getElementById("chk-face")  as HTMLInputElement;
const chkPose    = document.getElementById("chk-pose")  as HTMLInputElement;
const hostInput  = document.getElementById("osc-host")  as HTMLInputElement;
const portInput  = document.getElementById("osc-port")  as HTMLInputElement;

// ─── OSC addresses (hard-coded, must match server) ───────────────────────────

const HAND_LANDMARKS     = 21;
const HANDS_MAX          = 2;
const FACE_KEY_COUNT     = FACE_KEY_INDICES.length; // 136
const POSE_LANDMARKS = 33;

const ADDR_HAND_0_FLOATS = HAND_LANDMARKS * 3; // 63
const ADDR_HAND_1_FLOATS = HAND_LANDMARKS * 3; // 63
const ADDR_FACE_FLOATS   = FACE_KEY_COUNT  * 3; // 408
const ADDR_POSE_FLOATS   = POSE_LANDMARKS * 3; // 99

// ─── WebSocket ───────────────────────────────────────────────────────────────

const wsUrl = `${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws`;
let ws: WebSocket = connect();

function connect(): WebSocket {
  const socket = new WebSocket(wsUrl);
  socket.onopen  = () => setStatus("Connected");
  socket.onclose = () => {
    setStatus("Disconnected — retrying…");
    setTimeout(() => { ws = connect(); }, 2000);
  };
  socket.onmessage = (e) => {
    const msg = JSON.parse(e.data) as ToClient;
    if (msg.type === "status") setStatus(msg.message);
  };
  return socket;
}

function sendWs(msg: ToServer) {
  if (ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify(msg));
}

// ─── OSC Config ──────────────────────────────────────────────────────────────

function sendOscConfig() {
  sendWs({ type: "config", osc: { host: hostInput.value, port: Number(portInput.value) } });
}

hostInput.addEventListener("change", sendOscConfig);
portInput.addEventListener("change", sendOscConfig);

// ─── Task Checkboxes ─────────────────────────────────────────────────────────

chkHand.addEventListener("change", () => {
  //if (!chkHand.checked && !chkFace.checked) chkFace.checked = true;
  updateOscDebug(false, false, false, false);
});
chkFace.addEventListener("change", () => {
  //if (!chkHand.checked && !chkFace.checked) chkHand.checked = true;
  updateOscDebug(false, false, false, false);
});
chkHand.addEventListener("change", () => {
  //if (!chkHand.checked && !chkFace.checked) chkFace.checked = true;
  updateOscDebug(false, false, false, false);
})

// ─── MediaPipe Init ──────────────────────────────────────────────────────────

const WASM_URL   = "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/wasm";
const MODEL_BASE = "https://storage.googleapis.com/mediapipe-models";

async function initMediaPipe() {
  setStatus("Loading MediaPipe…");
  const vision = await FilesetResolver.forVisionTasks(WASM_URL);

  handLandmarker = await HandLandmarker.createFromModelPath(
    vision,
    `${MODEL_BASE}/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task`
  );
  await handLandmarker.setOptions({ runningMode: "VIDEO", numHands: 2 });

  faceLandmarker = await FaceLandmarker.createFromModelPath(
    vision,
    `${MODEL_BASE}/face_landmarker/face_landmarker/float16/1/face_landmarker.task`
  );
  await faceLandmarker.setOptions({ runningMode: "VIDEO" });
  
  poseLandmarker = await PoseLandmarker.createFromModelPath(
      vision,
      `${MODEL_BASE}/pose_landmarker/pose_landmarker_heavy/float16/1/pose_landmarker_heavy.task`
  );
  await poseLandmarker.setOptions({ runningMode: "VIDEO" });

  setStatus("Ready");
}

let handLandmarker: HandLandmarker | null = null;
let faceLandmarker: FaceLandmarker | null = null;
let poseLandmarker: PoseLandmarker | null = null;

// ─── Webcam ───────────────────────────────────────────────────────────────────

async function startCamera() {
  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  video.srcObject = stream;
  video.style.position = "absolute";
  video.style.left = "-9999px";
  video.style.width = "1px";
  video.style.height = "1px";
  canvas.style.transform = "scaleX(-1)";
  await new Promise<void>((res) => { video.onloadeddata = () => res(); });
}

// ─── Drawing helpers ─────────────────────────────────────────────────────────

function drawHands(result: HandLandmarkerResult) {
  const draw = new DrawingUtils(ctx);
  for (const landmarks of result.landmarks) {
    draw.drawConnectors(landmarks, HandLandmarker.HAND_CONNECTIONS, { color: "#00ff88", lineWidth: 2 });
    draw.drawLandmarks(landmarks, { color: "#ff0055", lineWidth: 1, radius: 3 });
  }
}

function drawFace(result: FaceLandmarkerResult) {
  const draw = new DrawingUtils(ctx);
  for (const landmarks of result.faceLandmarks) {
    draw.drawConnectors(landmarks, FaceLandmarker.FACE_LANDMARKS_TESSELATION,    { color: "#ffffff18", lineWidth: 1 });
    draw.drawConnectors(landmarks, FaceLandmarker.FACE_LANDMARKS_FACE_OVAL,      { color: "#4488ff88", lineWidth: 1 });
    draw.drawConnectors(landmarks, FaceLandmarker.FACE_LANDMARKS_RIGHT_EYE,      { color: "#ff446688", lineWidth: 1 });
    draw.drawConnectors(landmarks, FaceLandmarker.FACE_LANDMARKS_LEFT_EYE,       { color: "#44ff6688", lineWidth: 1 });
    draw.drawConnectors(landmarks, FaceLandmarker.FACE_LANDMARKS_RIGHT_EYEBROW,  { color: "#ff446688", lineWidth: 1 });
    draw.drawConnectors(landmarks, FaceLandmarker.FACE_LANDMARKS_LEFT_EYEBROW,   { color: "#44ff6688", lineWidth: 1 });
    draw.drawConnectors(landmarks, FaceLandmarker.FACE_LANDMARKS_LIPS,           { color: "#ffaa0088", lineWidth: 1 });

    for (let i = 0; i < landmarks.length; i++) {
      if (!FACE_KEY_INDEX_SET.has(i)) continue;
      const { x, y } = landmarks[i];
      ctx.beginPath();
      ctx.arc(x * canvas.width, y * canvas.height, 2.5, 0, Math.PI * 2);
      ctx.fillStyle = "#00eeff";
      ctx.fill();
    }
  }
}

function drawPose(result: PoseLandmarkerResult) {
  const draw = new DrawingUtils(ctx)
  for (const landmarks of result.landmarks) {
    draw.drawConnectors(landmarks, PoseLandmarker.POSE_CONNECTIONS, { color: "#00ff88", lineWidth: 2 });
    draw.drawLandmarks(landmarks, { color: "#ff0055", lineWidth: 1, radius: 3 });
  }
}


// ─── Render Loop ─────────────────────────────────────────────────────────────

let lastSentAt = 0;
const SEND_INTERVAL_MS = 1000 / 30;

function loop() {
  requestAnimationFrame(loop);
  if (video.readyState < HTMLMediaElement.HAVE_CURRENT_DATA) return;

  if (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
  }

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const now = performance.now();
  const throttle = now - lastSentAt > SEND_INTERVAL_MS;
  let hand0 = false, hand1 = false, face = false, pose = false;

  if (chkHand.checked && handLandmarker) {
    const result = handLandmarker.detectForVideo(video, now);
    drawHands(result);
    hand0 = result.landmarks.length > 0;
    hand1 = result.landmarks.length > 1;
    if (throttle) sendWs({ type: "landmarks", task: "hand", hands: result.landmarks });
  }

  if (chkFace.checked && faceLandmarker) {
    const result = faceLandmarker.detectForVideo(video, now);
    drawFace(result);
    face = result.faceLandmarks.length > 0;
    if (throttle) sendWs({ type: "landmarks", task: "face", face: result.faceLandmarks[0] });
  }
  
  if (chkPose.checked && poseLandmarker) {
    const result = poseLandmarker.detectForVideo(video, now);
    drawPose(result);
    pose = result.landmarks.length > 0;
    if (throttle) sendWs({ type: "landmarks", task: "pose", pose: result.landmarks });
  }

  if (throttle) {
    lastSentAt = now;
    updateOscDebug(hand0, hand1, face, pose);
  }
}

// ─── OSC Debug Panel ─────────────────────────────────────────────────────────

const col = 10;
dbgHand0.textContent = `/hand/0`.padEnd(col) + `${ADDR_HAND_0_FLOATS} floats   # hand 0: 21 landmarks × x y z  (zeros when not detected)`;
dbgHand1.textContent = `/hand/1`.padEnd(col) + `${ADDR_HAND_1_FLOATS} floats   # hand 1: 21 landmarks × x y z  (zeros when not detected)`;
dbgFace.textContent  = `/face`.padEnd(col)   + `${ADDR_FACE_FLOATS} floats  # 136 key points × x y z  (zeros when not detected)`;
dbgPose.textContent =  `/pose`.padEnd(col)   + `${ADDR_POSE_FLOATS} floats  # 33 landmarks × x y z  (zeros when not detected)`;

function setOscRowState(el: Element, enabled: boolean, sending: boolean) {
  el.classList.toggle("enabled", enabled && !sending);
  el.classList.toggle("sending", sending);
}

function updateOscDebug(hand0: boolean, hand1: boolean, face: boolean, pose: boolean) {
  setOscRowState(dbgHand0, chkHand.checked, chkHand.checked && hand0);
  setOscRowState(dbgHand1, chkHand.checked, chkHand.checked && hand1);
  setOscRowState(dbgFace,  chkFace.checked, chkFace.checked && face);
  setOscRowState(dbgPose, chkPose.checked, chkPose.checked && pose)
}

// ─── Utility ─────────────────────────────────────────────────────────────────

function setStatus(msg: string) {
  statusEl.textContent = msg;
}

// ─── Boot ─────────────────────────────────────────────────────────────────────

(async () => {
  updateOscDebug(false, false, false, false);
  await initMediaPipe();
  await startCamera();
  loop();
})().catch((err) => {
  console.error(err);
  setStatus(`Error: ${err.message}`);
});

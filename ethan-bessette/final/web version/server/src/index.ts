import express from "express";
import { createServer } from "node:http";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { WebSocketServer, WebSocket } from "ws";
import { Client, Message } from "node-osc";
import type { ToServer, ToClient } from "../../shared/types.js";
import { FACE_KEY_INDICES } from "../../shared/face-key-indices.js";

const PORT = 3001;
const CLIENT_DIST = path.resolve(fileURLToPath(import.meta.url), "../../../client/dist");

// Fixed OSC addresses
const ADDR_HAND_0 = "/hand/0";
const ADDR_HAND_1 = "/hand/1";
const ADDR_FACE = "/face";
const ADDR_POSE_PREFIX = "/pose";

const HAND_LANDMARKS = 21;
const POSE_LANDMARKS = 33;

const app = express();
app.use(express.static(CLIENT_DIST));

const httpServer = createServer(app);
const wss = new WebSocketServer({ server: httpServer });

let oscClient = new Client("127.0.0.1", 9000);

function send(ws: WebSocket, msg: ToClient) {
  ws.send(JSON.stringify(msg));
}

function handFloats(hand: { x: number; y: number; z: number }[] | undefined): number[] {
  const floats: number[] = [];
  for (let n = 0; n < HAND_LANDMARKS; n++) {
    const lm = hand?.[n];
    floats.push(lm?.x ?? 0, lm?.y ?? 0, lm?.z ?? 0);
  }
  return floats;
}

function poseFloats(pose: { x: number; y: number; z: number }[] | undefined): number[] {
  const floats: number[] = [];
  for (let n = 0; n < POSE_LANDMARKS; n++) {
    const lm = pose?.[n];
    floats.push(lm?.x ?? 0, lm?.y ?? 0, lm?.z ?? 0);
  }
  return floats;
}

wss.on("connection", (ws) => {
  console.log("Client connected");
  send(ws, { type: "status", message: "OSC → 127.0.0.1:9000" });

  ws.on("message", (raw) => {
    let msg: ToServer;
    try {
      msg = JSON.parse(raw.toString()) as ToServer;
    } catch {
      return;
    }

    if (msg.type === "config") {
      oscClient.close();
      oscClient = new Client(msg.osc.host, msg.osc.port);
      const status = `OSC → ${msg.osc.host}:${msg.osc.port}`;
      console.log(status);
      send(ws, { type: "status", message: status });
      return;
    }

    if (msg.type !== "landmarks") return;

    const osc = (m: Message) =>
        oscClient.send(m, (err: unknown) => {
          if (err) console.error("OSC send error:", err);
        });

    if (msg.task === "hand") {
      osc(new Message(ADDR_HAND_0, ...handFloats(msg.hands?.[0])));
      osc(new Message(ADDR_HAND_1, ...handFloats(msg.hands?.[1])));
      return;
    }

    if (msg.task === "face") {
      const floats: number[] = [];
      for (const n of FACE_KEY_INDICES) {
        const lm = msg.face?.[n];
        floats.push(lm?.x ?? 0, lm?.y ?? 0, lm?.z ?? 0);
      }
      osc(new Message(ADDR_FACE, ...floats));
      return;
    }

    if (msg.task === "pose") {
      const poses = msg.poses ?? [];
      for (let i = 0; i < poses.length; i++) {
        const floats = poseFloats(poses[i]);
        osc(new Message(`${ADDR_POSE_PREFIX}/${i}`, ...floats));
      }
    }
  });

  ws.on("close", () => console.log("Client disconnected"));
});

httpServer.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
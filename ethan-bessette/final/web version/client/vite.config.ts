import { defineConfig } from "vite";

export default defineConfig({
  server: {
    proxy: {
      "/ws": {
        target: "ws://localhost:3001",
        ws: true,
      },
    },
  },
  optimizeDeps: {
    exclude: ["@mediapipe/tasks-vision"],
  },
  build: {
    sourcemap: false,
  },
});

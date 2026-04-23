export type Landmark = { x: number; y: number; z: number }

export type ToServer =
  | { type: "config"; osc: { host: string; port: number } }
  | { type: "landmarks"; task: "hand" | "face" | "pose"; hands?: Landmark[][]; face?: Landmark[]; pose?: Landmark[] }

export type ToClient = { type: "status"; message: string }

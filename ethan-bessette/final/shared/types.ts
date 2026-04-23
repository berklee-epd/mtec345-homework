export type Landmark = { x: number; y: number; z: number }

export type ToServer =
    | {
    type: "config";
    osc: { host: string; port: number };
}
    | {
    type: "landmarks";
    task: "hand";
    hands?: { x: number; y: number; z: number }[][];
}
    | {
    type: "landmarks";
    task: "face";
    face?: { x: number; y: number; z: number }[];
}
    | {
    type: "landmarks";
    task: "pose";
    poses?: { x: number; y: number; z: number }[][];
};

export type ToClient =
    | {
    type: "status";
    message: string;
};

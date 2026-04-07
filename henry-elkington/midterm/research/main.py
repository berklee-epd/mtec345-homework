import argparse
import json
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn


# Model definitions ( must match notebook 02 and 04 )

class MLP(nn.Module):
    def __init__(self, n_features, hidden=128, dropout=0.2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_features, hidden),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden, hidden // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden // 2, 1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)


class GRUModel(nn.Module):
    def __init__(self, n_features, hidden=64, num_layers=1):
        super().__init__()
        self.gru = nn.GRU(n_features, hidden, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden, 1)

    def forward(self, x):
        x = x.unsqueeze(1)
        out, _ = self.gru(x)
        return torch.sigmoid(self.fc(out[:, -1, :])).squeeze(-1)


class LSTMModel(nn.Module):
    def __init__(self, n_features, hidden=64, num_layers=1):
        super().__init__()
        self.lstm = nn.LSTM(n_features, hidden, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden, 1)

    def forward(self, x):
        x = x.unsqueeze(1)
        out, _ = self.lstm(x)
        return torch.sigmoid(self.fc(out[:, -1, :])).squeeze(-1)


# GSI feature extraction

WEAPON_FEATURES = {
    "weapon_ak47": "weapon_ak47",
    "weapon_awp": "weapon_awp",
    "weapon_m4a1": "weapon_m4a4",
    "weapon_m4a1_silencer": "weapon_m4a4",
    "weapon_m4a4": "weapon_m4a4",
    "weapon_sg556": "weapon_sg553",
    "weapon_sg553": "weapon_sg553",
    "weapon_usp_silencer": "weapon_usps",
    "weapon_hkp2000": "weapon_usps",
}

GRENADE_FEATURES = {
    "weapon_hegrenade": "grenade_hegrenade",
    "weapon_flashbang": "grenade_flashbang",
    "weapon_smokegrenade": "grenade_smokegrenade",
    "weapon_incgrenade": "grenade_incendiarygrenade",
    "weapon_molotov": "grenade_incendiarygrenade",
}


def extract_features(data: dict, feature_order: list[str]) -> pd.DataFrame | None:
    """Extract model features from a GSI JSON payload."""
    allplayers = data.get("allplayers")
    if not allplayers:
        return None

    # bomb state
    bomb_planted = False
    bomb_info = data.get("bomb")
    if bomb_info and bomb_info.get("state") == "planted":
        bomb_planted = True
    round_info = data.get("round")
    if round_info and round_info.get("bomb") == "planted":
        bomb_planted = True

    # per side accumulators
    ct = {"health": 0, "armor": 0, "helmets": 0, "defuse_kits": 0, "players_alive": 0}
    t = {"health": 0, "armor": 0, "helmets": 0}

    # weapon and grenade counts
    wep_counts: dict[str, int] = {}
    for feat in feature_order:
        if "_weapon_" in feat or "_grenade_" in feat:
            wep_counts[feat] = 0

    for _pid, player in allplayers.items():
        team = player.get("team", "").upper()
        if team not in ("CT", "T"):
            continue

        state = player.get("state", {})
        health = state.get("health", 0)
        armor_val = state.get("armor", 0)
        helmet = state.get("helmet", False)
        defusekit = state.get("defusekit", False)
        side = "ct" if team == "CT" else "t"

        if side == "ct":
            ct["health"] += health
            ct["armor"] += armor_val
            if helmet:
                ct["helmets"] += 1
            if defusekit:
                ct["defuse_kits"] += 1
            if health > 0:
                ct["players_alive"] += 1
        else:
            t["health"] += health
            t["armor"] += armor_val
            if helmet:
                t["helmets"] += 1

        for _slot, wep in player.get("weapons", {}).items():
            wep_name = wep.get("name", "")
            if wep_name in WEAPON_FEATURES:
                key = f"{side}_{WEAPON_FEATURES[wep_name]}"
                if key in wep_counts:
                    wep_counts[key] += 1
            if wep_name in GRENADE_FEATURES:
                key = f"{side}_{GRENADE_FEATURES[wep_name]}"
                if key in wep_counts:
                    wep_counts[key] += 1

    # build row in feature_order
    row: dict[str, float] = {}
    for feat in feature_order:
        if feat == "bomb_planted":
            row[feat] = float(bomb_planted)
        elif feat == "ct_health":
            row[feat] = float(ct["health"])
        elif feat == "ct_armor":
            row[feat] = float(ct["armor"])
        elif feat == "t_armor":
            row[feat] = float(t["armor"])
        elif feat == "ct_helmets":
            row[feat] = float(ct["helmets"])
        elif feat == "t_helmets":
            row[feat] = float(t["helmets"])
        elif feat == "ct_defuse_kits":
            row[feat] = float(ct["defuse_kits"])
        elif feat == "ct_players_alive":
            row[feat] = float(ct["players_alive"])
        else:
            row[feat] = float(wep_counts.get(feat, 0))

    return pd.DataFrame([row], columns=feature_order)


# Display

BLUE = "\033[94m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def format_bar(ct_pct: float, width: int = 40) -> str:
    ct_fill = int(round(ct_pct / 100 * width))
    t_fill = width - ct_fill
    return f"{BLUE}{'█' * ct_fill}{RESET}{YELLOW}{'█' * t_fill}{RESET}"


frame_counter = 0
last_frame_time = 0.0


def print_predictions(predictions: dict[str, float]):
    """Print a formatted prediction block for all models."""
    global frame_counter, last_frame_time

    frame_counter += 1
    now = time.time()
    dt = now - last_frame_time if last_frame_time > 0 else 0
    last_frame_time = now

    # +1 for the status line
    n = len(predictions) + 1
    sys.stdout.write(f"\033[{n}A\033[J")

    dt_str = f"{dt:.1f}s ago" if dt > 0 else "0s ago"
    print(f"  {DIM}frame #{frame_counter} ({dt_str}){RESET}")

    for name, ct_pct in predictions.items():
        t_pct = 100 - ct_pct
        bar = format_bar(ct_pct)
        print(
            f"  {name:<20s} "
            f"{BLUE}CT {ct_pct:5.1f}%{RESET} "
            f"{bar} "
            f"{YELLOW}{t_pct:5.1f}% T{RESET}"
        )


# HTTP handler

class GSIHandler(BaseHTTPRequestHandler):
    models: dict = {}
    scaler = None
    feature_order: list[str] = []
    first_update = True

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        self.send_response(200)
        self.end_headers()

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return

        features = extract_features(data, self.feature_order)
        if features is None:
            return

        scaled = self.scaler.transform(features)
        scaled_tensor = torch.from_numpy(scaled).float()

        predictions: dict[str, float] = {}
        with torch.inference_mode():
            for name, model in self.models.items():
                if name == "Random Forest":
                    proba = model.predict_proba(scaled)[0]
                    ct_pct = proba[0] * 100
                else:
                    t_prob = model(scaled_tensor).item()
                    ct_pct = (1 - t_prob) * 100
                predictions[name] = ct_pct

        # print blank lines on first update so the cursor-up trick works
        if self.first_update:
            GSIHandler.first_update = False
            for _ in range(len(predictions) + 1):
                print()

        print_predictions(predictions)

    def log_message(self, _format, *_args):
        pass


# Model loading

def load_models(model_dir: Path, models_to_load: list[str] | None = None):
    """Load models from the model directory. Returns (models_dict, scaler, feature_order)."""
    config_path = model_dir / "model_configs.json"
    if not config_path.exists():
        print(f"Error: {config_path} not found. Run notebook 04 first.")
        sys.exit(1)

    config = json.loads(config_path.read_text())
    feature_order = config["features"]
    n_features = config["n_features"]

    scaler = joblib.load(model_dir / "scaler_final.joblib")

    all_models = {
        "Random Forest": ("rf_final.joblib", None),
        "MLP": ("mlp_final.pt", lambda: MLP(n_features, hidden=config["mlp"]["hidden"])),
        "GRU": ("gru_final.pt", lambda: GRUModel(n_features, hidden=config["gru"]["hidden"])),
        "LSTM": ("lstm_final.pt", lambda: LSTMModel(n_features, hidden=config["lstm"]["hidden"])),
    }

    if models_to_load:
        # Filter to requested models (case-insensitive match)
        lower_requested = [m.lower() for m in models_to_load]
        all_models = {
            k: v for k, v in all_models.items()
            if k.lower() in lower_requested or k.lower().replace(" ", "") in lower_requested
        }

    models = {}
    for name, (filename, constructor) in all_models.items():
        path = model_dir / filename
        if not path.exists():
            print(f"  Warning: {path} not found, skipping {name}")
            continue

        if filename.endswith(".joblib"):
            models[name] = joblib.load(path)
        else:
            model = constructor()
            model.load_state_dict(torch.load(path, weights_only=True))
            model.eval()
            # JIT trace for faster inference + fuses ops, removes Python overhead
            dummy = torch.randn(1, n_features)
            model = torch.jit.trace(model, dummy)
            models[name] = model
        print(f"  Loaded {name} from {filename}")

    return models, scaler, feature_order


# CLI

def main():
    parser = argparse.ArgumentParser(
        description="CS2 live round-win prediction server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  uv run python main.py                     # all models, default port
  uv run python main.py -p 4000             # custom port
  uv run python main.py -m rf mlp           # only Random Forest and MLP
  uv run python main.py --list              # show available models
""",
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=3000,
        help="port to listen on (default: 3000)",
    )
    parser.add_argument(
        "-m", "--models",
        nargs="+",
        metavar="MODEL",
        help="models to load (e.g. randomforest mlp gru lstm). Default: all",
    )
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=Path(__file__).parent / "models",
        help="directory containing exported models (default: ./models)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="list available models and exit",
    )

    args = parser.parse_args()

    if args.list:
        print("Available models:")
        print("  randomforest       — Random Forest (scikit-learn)")
        print("  mlp                — Multi-Layer Perceptron (PyTorch)")
        print("  gru                — Gated Recurrent Unit (PyTorch)")
        print("  lstm               — Long Short-Term Memory (PyTorch)")
        return

    print("Loading models...")
    models, scaler, feature_order = load_models(args.model_dir, args.models)

    if not models:
        print("Error: no models loaded. Run the notebooks first or check --model-dir.")
        sys.exit(1)

    GSIHandler.models = models
    GSIHandler.scaler = scaler
    GSIHandler.feature_order = feature_order

    print(f"\nListening on http://localhost:{args.port}")
    print(f"Models: {', '.join(models.keys())}")
    print("Waiting for CS2 game state data...\n")

    server = HTTPServer(("0.0.0.0", args.port), GSIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == "__main__":
    main()

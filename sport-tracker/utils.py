import json
import os
from datetime import datetime
from config import MOVEMENTS, MUSCLE_TARGETS

DATA_PATH = "data/current_week.json"
HISTORY_PATH = "data/history.json"
TARGETS_PATH = "data/targets.json"


def init_week():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_PATH):
        data = {
            "start_date": str(datetime.now().date()),
            "movements": {m: 0 for m in MOVEMENTS},
            "muscles": {m: 0 for m in MUSCLE_TARGETS}
        }
        save_current_week(data)

def load_current_week():
    init_week()
    try:
        with open(DATA_PATH, "r") as f:
            content = f.read().strip()
            if not content:
                raise ValueError("Empty JSON file")
            return json.loads(content)
    except (json.JSONDecodeError, ValueError):
        os.remove(DATA_PATH)
        init_week()
        with open(DATA_PATH, "r") as f:
            return json.load(f)


def save_current_week(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

def increment_movement(movement):
    data = load_current_week()
    data["movements"][movement] += 1
    for muscle in MOVEMENTS[movement]["muscles"]:
        data["muscles"][muscle] += 1
    save_current_week(data)

def reset_week():
    week_data = load_current_week()

    # Charger l'historique de manière safe
    history = []
    if os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH, "r") as f:
                content = f.read().strip()
                if content:
                    history = json.loads(content)
        except json.JSONDecodeError:
            history = []

    # Ajouter la semaine courante à l'historique
    history.append(week_data)

    # Sauvegarder l'historique
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)

    # Réinitialiser la semaine courante
    if os.path.exists(DATA_PATH):
        os.remove(DATA_PATH)


def increment_muscle(muscle):
    data = load_current_week()
    data["muscles"][muscle] += 1
    save_current_week(data)

def load_targets():
    if not os.path.exists(TARGETS_PATH):
        return None
    with open(TARGETS_PATH, "r") as f:
        return json.load(f)

def save_targets(targets):
    with open(TARGETS_PATH, "w") as f:
        json.dump(targets, f, indent=2)
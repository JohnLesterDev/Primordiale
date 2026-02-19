import os
import sys

try:
    import tomllib
except ImportError:
    import tomli as tomllib

BASE_DIR = sys.path[0]
CONFIG_PATH = os.path.join(BASE_DIR, "config.toml")

# NOTE: Speeds are now in PIXELS PER SECOND, not pixels per frame.
DEFAULT_CONFIG = {
    "window": {
        "fps": 120,
        "shake_intensity": 11,
        "shake_duration": 50
    },
    "physics": {
        "gravity": 1200.0  # Increased for dt (was 0.3)
    },
    "player": {
        "dimensions": [0.04, 0.04]
    },
    "food": {
        "dimensions": [0.02, 0.02]
    },
    "enemy": {
        "dimensions": [0.025, 0.025],
        "base_speed": 210.0,       # Increased for dt (was 1.7)
        "slow_down_factor": 1.9,
        "inflate_size": 25
    }
}

first_run = False
_config = {}

if not os.path.exists(CONFIG_PATH):
    _config = DEFAULT_CONFIG
    first_run = True
else:
    try:
        with open(CONFIG_PATH, "rb") as f:
            _config = tomllib.load(f)
    except Exception:
        _config = DEFAULT_CONFIG
        first_run = True

FPS = _config["window"]["fps"]
SHAKE_INTENSITY = _config["window"]["shake_intensity"]
SHAKE_DURATION = _config["window"]["shake_duration"]

GRAVITY = _config["physics"]["gravity"]
PLAYER_DIMEN = _config["player"]["dimensions"]
FOOD_DIMEN = _config["food"]["dimensions"]
ENEMY_DIMEN = _config["enemy"]["dimensions"]
ENEMY_SPEED = _config["enemy"]["base_speed"]
ENEMY_SLOW_DOWN_FACTOR = _config["enemy"]["slow_down_factor"]
ENEMY_INFLATE_SIZE = _config["enemy"]["inflate_size"]

def create_config_file():
    # ... (Same logic, just writes the new large numbers)
    toml_string = f"""
[window]
fps = {DEFAULT_CONFIG['window']['fps']}
shake_intensity = {DEFAULT_CONFIG['window']['shake_intensity']}
shake_duration = {DEFAULT_CONFIG['window']['shake_duration']}

[physics]
gravity = {DEFAULT_CONFIG['physics']['gravity']}

[player]
dimensions = {DEFAULT_CONFIG['player']['dimensions']}

[food]
dimensions = {DEFAULT_CONFIG['food']['dimensions']}

[enemy]
dimensions = {DEFAULT_CONFIG['enemy']['dimensions']}
base_speed = {DEFAULT_CONFIG['enemy']['base_speed']}
slow_down_factor = {DEFAULT_CONFIG['enemy']['slow_down_factor']}
inflate_size = {DEFAULT_CONFIG['enemy']['inflate_size']}
"""
    try:
        with open(CONFIG_PATH, "w") as f:
            f.write(toml_string.strip())
        global first_run
        first_run = False
    except IOError:
        pass
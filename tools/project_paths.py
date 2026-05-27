from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(os.environ.get("CHARACTER_ROOT", Path(__file__).resolve().parents[1])).resolve()
STATE = ROOT / "state"
SESSION = ROOT / "session"
MESSAGES = ROOT / "messages"
PROFILE = ROOT / "profile"
TOOLS = ROOT / "tools"
SCRIPTS = ROOT / "scripts"


def state_path(name: str) -> Path:
    return STATE / name


def log_path(name: str) -> Path:
    return STATE / name

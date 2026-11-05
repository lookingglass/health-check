import os
import subprocess

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_FILE = f"{PROJECT_DIR}/state/latest_OOM"
LOG_FILE = "/var/log/messages"


def get_latest_oom():
    result = subprocess.run(
        ["grep", "-i", "killed process", LOG_FILE],
        capture_output=True,
        text=True,
    )
    lines = result.stdout.strip().splitlines()
    return lines[-1] if lines else ""


def get_saved_oom():
    if not os.path.exists(STATE_FILE):
        return ""
    with open(STATE_FILE) as fd:
        return fd.read().strip()


def save_oom(value):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as fd:
        fd.write(value)


def get_values():
    latest = get_latest_oom()
    saved = get_saved_oom()

    if latest != saved:
        save_oom(latest)
        if latest:
            return "CRIT", latest
    return "OK", latest

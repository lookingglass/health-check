import os

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../state/boot_id")


def get_current_boot_id():
    with open('/proc/sys/kernel/random/boot_id', 'r') as f:
        return f.read().strip()


def check_reboot_detected():
    current = get_current_boot_id()
    with open(STATE_FILE, 'r') as f:
        saved = f.read().strip()

    with open(STATE_FILE, 'w') as f:
        f.write(current.strip())

    if saved != current:
        return True
    return False

import subprocess


def is_active(service):
    return subprocess.call(
        ["systemctl", "is-active", service],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ) == 00


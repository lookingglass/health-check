import os

import psutil
import yaml

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check_memory():
    with open(f'{PROJECT_DIR}/config/thresholds.yaml') as fd:
        limits = yaml.safe_load(fd)
        warn_value = limits["memory_thresholds"]["limits"]["warn"]
        crit_value = limits["memory_thresholds"]["limits"]["crit"]

        used_percent = psutil.virtual_memory().percent

        if used_percent > crit_value:
            return "CRIT", f"{used_percent:.2f}%"
        elif used_percent > warn_value:
            return "WARN", f"{used_percent:.2f}%"
        return "OK", f"{used_percent:.2f}%"
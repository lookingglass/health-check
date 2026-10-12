import os
import shutil
import yaml

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def format_gb(bytes_val):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024: return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024


def get_free_space():
    total, used, free = shutil.disk_usage('/')
    return format_gb(total), format_gb(used), format_gb(free)


def check_space():
    with open(f'{project_dir}/config/thresholds.yaml') as fd:
        limits = yaml.safe_load(fd)
        warn_value = limits["disk_thresholds"]["limits"]["warn"]
        crit_value = limits["disk_thresholds"]["limits"]["crit"]

        total, used, free = shutil.disk_usage('/')

        used_percent = (total - free) / total * 100

        if used_percent > crit_value:
            return f"[CRIT]", f"{used_percent:.2f}%"
        elif used_percent > warn_value:
            return f"WARN", f"{used_percent:.2f}%"
        return f"OK", f"{used_percent:.2f}%"

import multiprocessing
import os

import yaml

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_load_average():
    return os.getloadavg()


def get_cpu_count():
    cpu_count = multiprocessing.cpu_count()
    return cpu_count


def get_values():
    la1, la5, la15 = get_load_average()
    cpu_count = get_cpu_count()
    with open(f'{project_dir}/config/thresholds.yaml') as fd:
        limits = yaml.safe_load(fd)
        warn_value_1min = limits["cpu_thresholds"]["per_cpu_1min"]["warn"]
        crit_value_1min = limits["cpu_thresholds"]["per_cpu_1min"]["crit"]

        warn_value_15min = limits["cpu_thresholds"]["per_cpu_15min"]["warn"]
        crit_value_15min = limits["cpu_thresholds"]["per_cpu_15min"]["crit"]

        if la15 / cpu_count > crit_value_15min:
            return f"CRIT", la15, cpu_count
        if la1 / cpu_count > crit_value_1min:
            return f"CRIT", la1, cpu_count
        if la15 / cpu_count > warn_value_15min:
            return f"WARN", la15, cpu_count
        if la1 / cpu_count > warn_value_1min:
            return f"WARN", la1, cpu_count
        return "OK", la1, cpu_count

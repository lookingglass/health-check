import json
import os

import yaml

from checks import systemd, loadavg, free_space, reboot_detection, ssl_check

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open('./state/instance.txt', 'r') as f:
    instance = f.read()

load_average_status, load_average_1min, cpu_count = loadavg.get_values()

load_average = {
    "status": load_average_status,
    "1min_per_core": f"{load_average_1min / cpu_count:.2f}",
    "1min_total": f"{load_average_1min:.2f}",
}

disk_space_status, disk_space_used = free_space.check_space()
disk_status = {
    "status": disk_space_status,
    "space_used": disk_space_used,
}
reboot_detected = reboot_detection.check_reboot_detected()


def check_services():
    result = {}

    with open(f'./config/systemd_services.yaml') as fd:
        services = yaml.safe_load(fd)

    for service in services["services"]:
        is_active = systemd.is_active(service)
        result[service] = {
            "status": "OK" if is_active else "FAIL",
        }
    return result


with open(f'./config/endpoints.yaml') as endpoint:
    endpoints = yaml.safe_load(endpoint)

endpoint_checks = {}
for endpoint in endpoints["endpoints"]:
    host = endpoint["host"]
    port = endpoint["port"]

    endpoint_checks[host] = ssl_check(host, port)

report = {
    "instance": instance,
    "services": {"systemd_services": check_services(), "ssl_certs": endpoint_checks, },
    "reboot_detected": reboot_detected,
    "disk_usage": disk_status,
    "load_average": load_average,
}
result = json.dumps(report)
print(result)

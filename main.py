import json
import os

import yaml

from checks import systemd, loadavg, free_space, reboot_detection, ssl_check, get_status_code, memory, check_oom

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(PROJECT_DIR, "state", "instance.txt")) as f:
    instance = f.read().strip()

with open(os.path.join(PROJECT_DIR, "config", "systemd_services.yaml")) as f:
    services = yaml.safe_load(f)["services"]

with open(os.path.join(PROJECT_DIR, "config", "endpoints.yaml")) as f:
    config = yaml.safe_load(f)

endpoints = config.get("endpoints", [])

load_status, load_1min, cpu_count = loadavg.get_values()
disk_status, disk_used = free_space.check_space()
mem_status, mem_available = memory.check_memory()

ssl_certs = {}
status_codes = {}

for endpoint in endpoints:
    host = endpoint["host"]
    port = endpoint.get("port", 443)

    for check in endpoint.get("checks", []):
        check_type = check["type"]

        if check_type == "ssl":
            ssl_certs[host] = ssl_check(host, port)

        elif check_type == "status_code":
            get_status_code(host, port, expected=check.get("expected"))

report = {
    "instance": instance,
    "services": {
        "systemd_services": {
            name: {"status": "OK" if systemd.is_active(name) else "FAIL"}
            for name in services
        },
        "ssl_certs": ssl_certs,
        "status_codes": status_codes,
    },
    "reboot_detected": reboot_detection.check_reboot_detected(),
    "memory" : {
        "status": mem_status,
        "usage": mem_available

    },
    "disk_usage": {
        "status": disk_status,
        "space_used": disk_used
    },
    "load_average": {
        "status": load_status,
        "1min_per_core": f"{load_1min / cpu_count:.2f}",
        "1min_total": f"{load_1min:.2f}",
    },
}

print(json.dumps(report))
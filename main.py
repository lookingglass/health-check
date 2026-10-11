import json

from checks import systemd, loadavg, free_space, reboot_detection

systemd_services_to_check = ["docker.service", "gitlab-runner.service", "fake.service"] # define services // todo move services to ./config/systemd-services.yaml
service_checks = {}
with open('./state/instance.txt', 'r') as f:
    instance = f.read()


load_average = loadavg.get_values()
free_sp = free_space.check_space()
reboot_detected = reboot_detection.check_reboot_detected()
for service in systemd_services_to_check:
    is_active = systemd.is_active(service)
    service_checks[service] = {
        "status": "OK" if is_active else "FAIL",
    }

report = {
    "instance": instance,
    "services": service_checks,
    "reboot_detected": reboot_detected,
    "free_space": free_sp,
    "load_average": load_average,
}
result = json.dumps(report)
print(result)

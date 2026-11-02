import os
import requests

import yaml

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_status_code(domain: str, port: int, expected: list = None):
    try:
        with open(f"{PROJECT_DIR}/config/endpoints.yaml") as fd:
            config = yaml.safe_load(fd)

        http_settings = config["settings"]["http"]
        timeout = http_settings["timeout"]
        follow_redirects = http_settings["follow_redirects"]

        if not expected:
            expected = [200]

        response = requests.get(
            f"https://{domain}:{port}",
            timeout=timeout,
            allow_redirects=follow_redirects
        )
        if response.status_code in expected:
            return {
                "status": "OK",
                "status_code": response.status_code
            }

        return {
            "status": "CRIT",
            "status_code": response.status_code,
            "expected": expected
        }

    except requests.exceptions.Timeout:
        return {"status": "Error: timeout"}

    except requests.exceptions.ConnectionError:
        return {"status": "Error: Failed to reach server"}

    except requests.exceptions.RequestException as e:
        return {"status": f"Error: {str(e)}"}
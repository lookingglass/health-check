import os
import ssl
import socket

from datetime import datetime

import yaml

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ssl_check(domain: str, port: int):
    try:
        with socket.create_connection((domain, port), timeout=2) as sock:
            with ssl.create_default_context().wrap_socket(
                    sock, server_hostname=domain
            ) as tls:
                ssl_data = {
                    "issued": tls.getpeercert()["notBefore"],
                    "expires": datetime.strptime(
                        tls.getpeercert()["notAfter"], "%b %d %H:%M:%S %Y GMT"
                    ).strftime("%Y-%m-%d"),
                }
                expires = datetime.strptime(ssl_data["expires"], "%Y-%m-%d")
                days_left = (expires - datetime.now()).days

                with open(f'{project_dir}/config/endpoints.yaml') as fd:
                    limits = yaml.safe_load(fd)
                    warn_value = limits["settings"]["ssl"]["warn_days"]
                    crit_value = limits["settings"]["ssl"]["crit_days"]

                if days_left < crit_value:
                    return {"status": "CRIT", "days_left": days_left}
                if days_left < warn_value:
                    return {"status": "WARN", "days_left": days_left}
                else:
                    return {"status": "OK"}
    except socket.timeout:
        return {"status": "Error: timeout"}
    except socket.gaierror:
        return {"status": "Error: Failed to reach server"}
    except ssl.SSLError as e:
        return {"status": f"Error: {str(e)}"}

import ssl
import socket

from datetime import datetime


WARN_DAYS_LEFT = 14
CRIT_DAYS_LEFT = 7


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

                if days_left < CRIT_DAYS_LEFT:
                    return {"status": "CRIT", "days_left": days_left}
                if days_left < WARN_DAYS_LEFT:
                    return {"status": "WARN", "days_left": days_left}
                else:
                    return {"status": "OK"}
    except socket.timeout:
        return {"status": "Error: timeout"}
    except socket.gaierror:
        return {"status": "Error: Failed to reach server"}
    except ssl.SSLError as e:
        return {"status": f"Error: {str(e)}"}

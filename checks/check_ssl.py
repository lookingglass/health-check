import ssl
import socket



def ssl_check(domain: str, port: int):
    try:
        with socket.create_connection((domain, port), timeout=2) as sock:
            with ssl.create_default_context().wrap_socket(
                    sock, server_hostname=domain
            ) as tls:
                ssl_data = {
                    "issued": tls.getpeercert()["notBefore"],
                    "expires": tls.getpeercert()["notAfter"],
                }
                return ssl_data
    except socket.timeout:
        return {"error": "timeout"}
    except socket.gaierror:
        return {"error": "Failed to reach server"}
    except ssl.SSLError as e:
        return {"error": str(e)}


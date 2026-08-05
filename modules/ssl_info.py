import socket
import ssl
from datetime import datetime

from utils.ui import title, section, success, error, warning, info


def ssl_information(target):

    title("SSL Information")

    info("Connecting to target...")

    try:

        context = ssl.create_default_context()

        with socket.create_connection((target, 443), timeout=5) as sock:

            with context.wrap_socket(sock, server_hostname=target) as secure_socket:

                cert = secure_socket.getpeercert()

                tls_version = secure_socket.version()

                cipher = secure_socket.cipher()[0]

        subject = dict(item[0] for item in cert["subject"])
        issuer = dict(item[0] for item in cert["issuer"])

        valid_from = datetime.strptime(
            cert["notBefore"],
            "%b %d %H:%M:%S %Y %Z"
        )

        valid_until = datetime.strptime(
            cert["notAfter"],
            "%b %d %H:%M:%S %Y %Z"
        )

        days_remaining = (valid_until - datetime.utcnow()).days

        section("Certificate Information")

        success(f"Common Name     : {subject.get('commonName', 'Unknown')}")
        success(f"Issuer          : {issuer.get('commonName', 'Unknown')}")
        success(f"Valid From      : {valid_from.date()}")
        success(f"Valid Until     : {valid_until.date()}")
        success(f"Days Remaining  : {days_remaining}")

        section("TLS Information")

        success(f"TLS Version     : {tls_version}")
        success(f"Cipher          : {cipher}")

        section("Security Analysis")

        if days_remaining <= 0:

            error("Certificate Status : EXPIRED")

        elif days_remaining <= 30:

            warning(f"Certificate expires in {days_remaining} days.")

        else:

            success("Certificate Status : VALID")

        success("HTTPS Enabled")

    except Exception as e:

        error(str(e))
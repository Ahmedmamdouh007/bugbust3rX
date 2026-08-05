import socket

from utils.ui import title, section, success, error, info


def dns_lookup(target):
    title("DNS Lookup")

    info("Resolving target...")

    try:
        ip = socket.gethostbyname(target)

        section("DNS Information")

        success(f"Target Domain : {target}")
        success(f"IP Address    : {ip}")

    except socket.gaierror:
        error("Failed to resolve target.")
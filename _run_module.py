"""
Internal helper: runs a single bugbust3rX module and prints its output
normally. Invoked as its own subprocess by run_full_recon.py so that
concurrent modules never share stdout (avoids the thread-safety issues
of redirecting a single global sys.stdout from multiple threads).

Usage: python3 _run_module.py <module_key> <target> [choice]
"""

import sys

from modules.dns_lookup import dns_lookup
from modules.whois_lookup import whois_lookup
from modules.http_headers import http_headers
from modules.banner_grab import banner_grab
from modules.port_scanner import port_scanner
from modules.ssl_info import ssl_information
from modules.security_headers import security_headers
from modules.technology_detection import technology_detection
from modules.subdomain_enum import subdomain_enum

REGISTRY = {
    "dns": lambda t, c: dns_lookup(t),
    "whois": lambda t, c: whois_lookup(t),
    "http_headers": lambda t, c: http_headers(t),
    "security_headers": lambda t, c: security_headers(t),
    "ssl": lambda t, c: ssl_information(t),
    "banner": lambda t, c: banner_grab(t),
    "tech": lambda t, c: technology_detection(t),
    "ports": lambda t, c: port_scanner(t, c),
    "subs": lambda t, c: subdomain_enum(t, c),
}


def main():
    key = sys.argv[1]
    target = sys.argv[2]
    choice = sys.argv[3] if len(sys.argv) > 3 else None

    fn = REGISTRY.get(key)
    if fn is None:
        print(f"[!] Unknown module key: {key}")
        sys.exit(1)

    try:
        fn(target, choice)
    except Exception as e:
        print(f"[!] Module '{key}' crashed: {e}")


if __name__ == "__main__":
    main()

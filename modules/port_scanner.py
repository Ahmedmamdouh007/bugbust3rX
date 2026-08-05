import subprocess
import shutil
import sys
import time
import contextlib

from yaspin import yaspin
from tabulate import tabulate

from utils.ui import title, section, success, error, info


def port_scanner(target, choice=None):

    title("Port Scanner")

    if shutil.which("nmap") is None:
        error("Nmap is not installed.")
        return []

    section("Scan Options")

    print("[1] Quick Scan (Top 100 Ports)")
    print("[2] Standard Scan (1-1024)")
    print("[3] Full Scan (1-65535)")

    if choice is None:
        choice = input("\nSelect Scan Type: ")
    else:
        print(f"\nSelect Scan Type: {choice}  (auto)")

    # --max-retries / --host-timeout bound worst-case runtime: without
    # them, nmap can spend minutes retransmitting to ports that never
    # answer (firewalled/filtered ports), which makes scans against
    # real-world hardened targets hang far longer than expected.
    if choice == "1":
        command = [
            "nmap",
            "-Pn",
            "-T4",
            "-sV",
            "--max-retries", "2",
            "--host-timeout", "90s",
            "--top-ports",
            "100",
            target
        ]
        scan_name = "Quick Scan"

    elif choice == "3":
        command = [
            "nmap",
            "-Pn",
            "-T4",
            "-sV",
            "--max-retries", "2",
            "--host-timeout", "600s",
            "-p-",
            target
        ]
        scan_name = "Full Scan"

    else:
        command = [
            "nmap",
            "-Pn",
            "-T4",
            "-sV",
            "--max-retries", "2",
            "--host-timeout", "180s",
            "-p",
            "1-1024",
            target
        ]
        scan_name = "Standard Scan"

    info("Preparing scanner...")

    start_time = time.time()

    # yaspin can't animate in place when stdout isn't a real terminal
    # (e.g. run non-interactively from Full Scan / a subprocess pipe) --
    # it falls back to printing every animation frame as its own line,
    # which floods captured/redirected output. Skip the spinner in that
    # case and just print a single status line instead.
    interactive = sys.stdout.isatty()

    spinner_ctx = (
        yaspin(text="Scanning target...", color="cyan")
        if interactive
        else contextlib.nullcontext()
    )

    if not interactive:
        info("Scanning target (this may take a moment)...")

    with spinner_ctx as spinner:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if interactive:
            spinner.ok("✔")
        else:
            success("Scan complete.")

    end_time = time.time()

    scan_time = round(end_time - start_time, 2)

    output = result.stdout.splitlines()

    open_ports = []

    services = set()

    for line in output:

        if "/tcp" in line and "open" in line:

            parts = line.split()

            if len(parts) < 3:
                continue

            port = parts[0]
            state = parts[1]
            service = parts[2]

            if len(parts) > 3:
                version = " ".join(parts[3:])
            else:
                version = "Unknown"

            open_ports.append([
                port,
                state.upper(),
                service.upper(),
                version
            ])

            services.add(service.upper())

    section("Open Ports")

    if open_ports:

        print(
            tabulate(
                open_ports,
                headers=[
                    "Port",
                    "State",
                    "Service",
                    "Version"
                ],
                tablefmt="grid"
            )
        )

    else:

        error("No open ports found.")

    section("Scan Summary")

    success(f"Open Ports : {len(open_ports)}")

    success(f"Scan Time  : {scan_time} Seconds")

    info(f"Scan Type   : {scan_name}")

    print()

    if services:

        info("Detected Services")

        for service in sorted(services):
            print(f"  • {service}")

    return open_ports
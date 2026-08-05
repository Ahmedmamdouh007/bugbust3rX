"""
full_scan.py
Runs all 9 bugbust3rX modules against ONE target in parallel (each as its
own subprocess, so output never gets mixed up between modules), asking the
user once whether they want a Passive or Active scan, and merges everything
into a single templated report file.

Can be called from main.py's menu via full_scan(target), or run standalone:
    python3 full_scan.py example.com
"""

import argparse
import os
import re
import subprocess
import sys
import time

from utils.ui import title, section, success, info, warning

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

# key -> (display name, needs a scan-mode arg?)
MODULES = [
    ("dns",              "DNS Lookup",             False),
    ("whois",            "WHOIS Lookup",           False),
    ("http_headers",     "HTTP Header Analysis",   False),
    ("security_headers", "Security Headers",       False),
    ("ssl",              "SSL Information",        False),
    ("banner",           "Banner Grabbing",        False),
    ("tech",             "Technology Detection",   False),
    ("ports",            "Port Scanner",           True),
    ("subs",             "Subdomain Enumeration",  True),
]


def strip_ansi(text):
    return ANSI_RE.sub("", text)


def _ask_mode():
    """Single Passive/Active prompt that drives both Port Scanner and
    Subdomain Enumeration for the whole Full Scan."""
    section("Full Scan Mode")
    print("[1] Passive  (fast: top-100 ports, passive subdomain sources only)")
    print("[2] Active   (thorough: full 1-65535 port scan, + amass)")

    while True:
        choice = input("\nSelect scan mode: ").strip()
        if choice in ("1", "2"):
            return choice
        warning("Invalid choice, enter 1 or 2.")


def _launch_all(target, mode, script_dir):
    # mode "1" (Passive) -> ports=1 (top-100), subs=1 (passive)
    # mode "2" (Active)  -> ports=3 (full range), subs=2 (active, adds amass)
    port_choice = "1" if mode == "1" else "3"
    sub_choice = "1" if mode == "1" else "2"
    module_arg = {"ports": port_choice, "subs": sub_choice}

    procs = {}
    for key, name, needs_arg in MODULES:
        cmd = [sys.executable, os.path.join(script_dir, "_run_module.py"), key, target]
        if needs_arg:
            cmd.append(module_arg[key])
        procs[key] = (name, time.time(),
                      subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, text=True))
    return procs


def _collect(procs):
    results = {}
    for key, (name, start, proc) in procs.items():
        output, _ = proc.communicate()
        elapsed = round(time.time() - start, 2)
        results[name] = strip_ansi(output)
        success(f"{name:<25} done in {elapsed}s")
    return results


def _write_report(target, mode, results, script_dir):
    reports_dir = os.path.join(script_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(reports_dir, f"full_scan_{target}_{timestamp}.txt")
    mode_label = "Passive" if mode == "1" else "Active"

    with open(path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("bugbust3rX - Full Scan Report\n")
        f.write(f"Target     : {target}\n")
        f.write(f"Scan Mode  : {mode_label}\n")
        f.write(f"Generated  : {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n")
        f.write("\nTable of Contents\n" + "-" * 70 + "\n")
        for _, name, _ in MODULES:
            f.write(f"  - {name}\n")
        f.write("\n")

        for _, name, _ in MODULES:
            f.write("\n" + "#" * 70 + "\n")
            f.write(f"# {name}\n")
            f.write("#" * 70 + "\n\n")
            f.write(results.get(name, "[!] No output captured.\n"))
            f.write("\n")

    return path


def full_scan(target):
    """Entry point called from main.py's menu."""
    title("Full Scan")

    mode = _ask_mode()
    mode_label = "Passive" if mode == "1" else "Active"

    script_dir = os.path.dirname(os.path.abspath(__file__))

    section("Running All 9 Modules")
    info(f"Mode: {mode_label} | Launching all modules in parallel...\n")

    start = time.time()
    procs = _launch_all(target, mode, script_dir)
    results = _collect(procs)
    path = _write_report(target, mode, results, script_dir)
    total = round(time.time() - start, 2)

    section("Full Scan Summary")
    success(f"All 9 modules completed in {total}s")
    success(f"Report saved to: {path}")

    return path


def main():
    parser = argparse.ArgumentParser(description="Run all bugbust3rX modules in parallel, merge into one report.")
    parser.add_argument("target", help="Target domain, e.g. example.com")
    args = parser.parse_args()
    full_scan(args.target)


if __name__ == "__main__":
    main()

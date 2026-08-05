![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Platform](https://img.shields.io/badge/Platform-Linux-green)
![License](https://img.shields.io/badge/License-MIT-orange)

# bugbust3rX

A modular Python reconnaissance framework for penetration testing, bug bounty recon, and security assessments — 9 recon tools you can run individually, or all at once in parallel as a single **Full Scan** that merges every result into one report file.


---

## Features

| # | Module | What it does |
|---|--------|---------------|
| 1 | DNS Lookup | Resolves the target domain to its IP address |
| 2 | WHOIS Lookup | Registrar, creation/expiry dates, name servers |
| 3 | HTTP Header Analysis | Fetches response headers, flags missing security headers |
| 4 | Port Scanner | nmap-backed scan — Quick (top 100), Standard (1-1024), or Full (1-65535) |
| 5 | Banner Grabbing | Grabs service banners on common ports (21, 22, 25, 80, 110, 143, 443) |
| 6 | SSL Information | Certificate details, expiry countdown, TLS version & cipher |
| 7 | Security Headers | Dedicated check against 6 key security headers |
| 8 | Technology Detection | Guesses CMS/framework/server from headers + HTML |
| 9 | Subdomain Enumeration | subfinder + sublist3r (+ amass in Active mode), with liveness checks |
| — | Directory Enumeration | *Coming soon — not yet implemented* |
| **11** | **Full Scan** | **Runs all 9 modules above in parallel and merges everything into one report** |

---

## How Full Scan works

Selecting **Full Scan** from the menu:

1. Asks **once** — Passive or Active:
   - **Passive**: top-100 port scan, subdomain enum from passive sources only (subfinder + sublist3r). Fast.
   - **Active**: full 1–65535 port scan, subdomain enum also runs amass. Thorough, slower.
2. Launches all 9 modules **at the same time**, each as its own isolated subprocess (not threads — this avoids output from different modules getting scrambled together, since Python's stdout redirection isn't safe to share across concurrent threads).
3. Waits for all 9 to finish, then writes one file: `reports/full_scan_<target>_<timestamp>.txt`, with a header, table of contents, and every module's output in a fixed, readable order — regardless of which order they actually finished in.

No further prompts once you've picked Passive/Active — it's fully automated from there.

---

## Prerequisites

Python packages are handled by `requirements.txt` (see below), but several modules shell out to external CLI tools that must be installed and on your `PATH` separately:

| Tool | Used by | Install |
|------|---------|---------|
| `nmap` | Port Scanner | `sudo apt install nmap` |
| `subfinder` | Subdomain Enumeration | [ProjectDiscovery releases](https://github.com/projectdiscovery/subfinder/releases) |
| `sublist3r` | Subdomain Enumeration | `pip install git+https://github.com/aboul3la/Sublist3r.git` |
| `amass` | Subdomain Enumeration (Active mode only) | [OWASP Amass releases](https://github.com/owasp-amass/amass/releases) |

Missing tools don't crash the scan — each module checks for its dependency and reports it as unavailable instead of failing the whole run.

---

## Installation

```bash
git clone https://github.com/Ahmedmamdouh007/bugbust3rX.git
cd bugbust3rX

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

deactivate

chmod +x install.sh
./install.sh
```

`install.sh` copies a `bugbust3rX` launcher into `/usr/local/bin`, so you can run it from anywhere afterward.

---

## Usage

### Interactive menu (all 11 options)

```bash
bugbust3rX
```

You'll be asked for a target domain once, then can run any module from the menu as many times as you like:

```
[1]  DNS Lookup
[2]  WHOIS Lookup
[3]  HTTP Header Analysis
[4]  Port Scanner
[5]  Banner Grabbing
[6]  SSL Information
[7]  Security Headers
[8]  Technology Detection
[9]  Subdomain Enumeration
[10] Directory Enumeration
[11] Full Scan (all 9 tools, parallel)
[0]  Exit
```

### Full Scan as a standalone command

You don't have to go through the menu — `full_scan.py` runs on its own too:

```bash
python3 full_scan.py example.com
```

This still prompts once for Passive/Active, runs all 9 modules in parallel, and writes the same merged report to `reports/`.

### Running from source without installing

```bash
python3 main.py
```

---

## Project Structure

```text
bugbust3rX/
│
├── main.py              # Interactive menu / entry point
├── full_scan.py          # Full Scan orchestrator (parallel, single report)
├── _run_module.py        # Internal dispatcher — runs one module as an isolated subprocess
├── modules/               # One file per recon tool
│   ├── dns_lookup.py
│   ├── whois_lookup.py
│   ├── http_headers.py
│   ├── security_headers.py
│   ├── ssl_info.py
│   ├── banner_grab.py
│   ├── technology_detection.py
│   ├── port_scanner.py
│   └── subdomain_enum.py
├── utils/
│   ├── colors.py          # Color palette
│   └── ui.py               # Shared print helpers (title, section, success, error, warning, info)
├── reports/                # Full Scan output lands here (git-ignored)
├── install.sh
├── bugbust3rX               # Launcher script installed to /usr/local/bin
├── requirements.txt
└── README.md
```

---

## Sample report layout

```text
======================================================================
bugbust3rX - Full Scan Report
Target     : example.com
Scan Mode  : Passive
Generated  : 2026-08-04 19:36:10
======================================================================

Table of Contents
----------------------------------------------------------------------
  - DNS Lookup
  - WHOIS Lookup
  ...

######################################################################
# DNS Lookup
######################################################################
[+] Target Domain : example.com
[+] IP Address    : 93.184.216.34
...
```

---

## Known limitations

- WHOIS and Subdomain Enumeration depend on external services (WHOIS servers, crt.sh-style sources, search engines) — results will vary depending on your network's outbound access and any firewalls in between.
- Port Scanner and Banner Grabbing need direct outbound TCP access to arbitrary ports on the target; behind a restrictive proxy/firewall, expect filtered/timeout results rather than a crash.
- Directory Enumeration is not implemented yet.

---

## Disclaimer

This tool is intended for educational purposes and **authorized** security testing only. Only run it against targets you own or have explicit written permission to test.

---



Licensed under MIT — see `LICENSE`.

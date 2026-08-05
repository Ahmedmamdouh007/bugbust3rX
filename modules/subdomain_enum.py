import subprocess
import shutil
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
from tabulate import tabulate
from utils.ui import title, section, success, error

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def _tool_exists(name):
    return shutil.which(name) is not None

def _run(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        return p.stdout.splitlines() if p.returncode == 0 else []
    except Exception:
        return []

def _subfinder(domain):
    return [x.strip() for x in _run(["subfinder","-silent","-d",domain]) if "." in x]

def _sublist3r(domain):
    outfile="/tmp/bugbust3rx_subs.txt"
    _run(["sublist3r","-d",domain,"-o",outfile])
    try:
        with open(outfile,"r") as f:
            return [x.strip() for x in f if "." in x]
    except Exception:
        return []

def _amass(domain):
    return [x.strip() for x in _run(["amass","enum","-passive","-d",domain]) if "." in x]

def _alive(host):
    for proto in ("https://","http://"):
        try:
            r=requests.get(proto+host,timeout=3,verify=False,allow_redirects=True)
            if r.status_code < 600:
                return True
        except Exception:
            pass
    return False

def subdomain_enum(domain, choice=None):
    title("Subdomain Enumeration")
    print("[1] Passive Scan")
    print("[2] Active Scan")
    if choice is None:
        choice = input("\nSelect Scan Type: ").strip()
    else:
        print(f"\nSelect Scan Type: {choice}  (auto)")

    section("Discovery")
    subs=[]

    if _tool_exists("subfinder"):
        subs.extend(_subfinder(domain))
    else:
        error("subfinder not found")

    if _tool_exists("sublist3r"):
        subs.extend(_sublist3r(domain))
    else:
        error("sublist3r not found")

    if choice=="2" and _tool_exists("amass"):
        subs.extend(_amass(domain))

    subs=sorted(set([s for s in subs if s.endswith(domain)]))

    success(f"Discovered {len(subs)} unique subdomains.")

    section("Validating Hosts")
    alive=[]
    with ThreadPoolExecutor(max_workers=25) as ex:
        fut={ex.submit(_alive,s):s for s in subs}
        for f in as_completed(fut):
            if f.result():
                alive.append(fut[f])

    table=[[s,"Alive" if s in alive else "Dead"] for s in subs]
    print(tabulate(table,headers=["Subdomain","Status"],tablefmt="grid"))

    section("Summary")
    success(f"Total : {len(subs)}")
    success(f"Alive : {len(alive)}")
    success(f"Dead  : {len(subs)-len(alive)}")

    import os

    os.makedirs("reports", exist_ok=True)

    with open("reports/subdomains.txt", "w") as f:
        for host in alive:
            f.write(host + "\n")
            
    return alive

from utils.colors import *

from modules.dns_lookup import dns_lookup
from modules.whois_lookup import whois_lookup
from modules.http_headers import http_headers
from modules.banner_grab import banner_grab
from modules.port_scanner import port_scanner
from modules.ssl_info import ssl_information
from modules.security_headers import security_headers
from modules.technology_detection import technology_detection
from modules.subdomain_enum import subdomain_enum
from full_scan import full_scan


def banner():

    print(RED + "=" * 65)

    print(RED + r"""
 _                 _               _   _____    __  __
| |__  _   _  __ _| |__  _   _ ___| |_|___ / _ _\ \/ /
| '_ \| | | |/ _` | '_ \| | | / __| __| |_ \| '__\  / 
| |_) | |_| | (_| | |_) | |_| \__ \ |_ ___) | |  /  \ 
|_.__/ \__,_|\__, |_.__/ \__,_|___/\__|____/|_| /_/\_\
             |___/
""")

    print(GREEN + "                    bugbust3rX v1.0")
    print(YELLOW + "       Automated Reconnaissance & Vuln-Recon Framework")
    print(MAGENTA + "     Based on ReconForge by Amr Abdelnabi -- Rebuilt by Ahmed Mamdouh")
    print(CYAN + "              For Educational / Authorized Use Only")
    print(RED + "=" * 65)


def menu():

    print()

    print(GREEN + "[1]  DNS Lookup")
    print(GREEN + "[2]  WHOIS Lookup")
    print(GREEN + "[3]  HTTP Header Analysis")
    print(GREEN + "[4]  Port Scanner")
    print(GREEN + "[5]  Banner Grabbing")
    print(GREEN + "[6]  SSL Information")
    print(GREEN + "[7]  Security Headers")
    print(GREEN + "[8]  Technology Detection")
    print(GREEN + "[9]  Subdomain Enumeration")
    print(GREEN + "[10] Directory Enumeration")
    print(CYAN + "[11] Full Scan (all 9 tools, parallel)")
    print(RED + "[0]  Exit")


def under_development():

    print()
    print(YELLOW + "=" * 60)
    print(YELLOW + "Me and AI are still trying to make it behave😂.")
    print(YELLOW + "=" * 60)

    input("\nPress Enter to continue...")


def main():

    banner()

    target = input(CYAN + "\nEnter target domain: ").strip()

    while True:

        banner()

        print(CYAN + f"\n🎯 Current Target : {target}")

        menu()

        choice = input(WHITE + "\nSelect an option: ").strip()

        if choice == "1":

            dns_lookup(target)
            input("\nPress Enter to continue...")

        elif choice == "2":

            whois_lookup(target)
            input("\nPress Enter to continue...")

        elif choice == "3":

            http_headers(target)
            input("\nPress Enter to continue...")

        elif choice == "4":

            port_scanner(target)
            input("\nPress Enter to continue...")

        elif choice == "5":

            banner_grab(target)
            input("\nPress Enter to continue...")

        elif choice == "6":

            ssl_information(target)
            input("\nPress Enter to continue...")

        elif choice == "7":

            security_headers(target)
            input("\nPress Enter to continue...")

        elif choice == "8":

            technology_detection(target)
            input("\nPress Enter to continue...")

        elif choice == "9":

            subdomain_enum(target)
            input("\nPress Enter to continue...")

        elif choice == "10":

            under_development()

        elif choice == "11":

            full_scan(target)
            input("\nPress Enter to continue...")

        elif choice == "0":

            print(YELLOW + "\n👋 Gracias!")
            break

        else:

            print(RED + "\n[-] Invalid option.")

            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
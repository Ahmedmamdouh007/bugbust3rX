from utils.colors import *


def line():
    print(CYAN + "=" * 60)


def title(text):
    line()
    print(MAGENTA + text.center(60))
    line()


def section(text):
    print()
    print(YELLOW + "-" * 60)
    print(YELLOW + text)
    print(YELLOW + "-" * 60)


def success(text):
    print(GREEN + "[+] " + text)


def error(text):
    print(RED + "[-] " + text)


def warning(text):
    print(YELLOW + "[!] " + text)


def info(text):
    print(CYAN + "[*] " + text)
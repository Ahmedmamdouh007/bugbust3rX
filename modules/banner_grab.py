import socket

from utils.ui import title, section, success, error, info


def banner_grab(target):

    title("Banner Grabbing")

    info("Connecting to target...")

    ports = [21, 22, 25, 80, 110, 143, 443]

    section("Open Service Banners")

    found = False

    for port in ports:

        try:

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)

            sock.connect((target, port))

            try:
                banner = sock.recv(1024).decode(errors="ignore").strip()

            except:
                banner = ""

            if banner:

                success(f"Port {port:<5} : {banner}")

            else:

                success(f"Port {port:<5} : Connected (No Banner)")

            found = True

            sock.close()

        except:

            continue

    if not found:

        error("No banners were collected.")
import requests

from utils.ui import title, section, success, error, warning, info

IMPORTANT_HEADERS = [
    "Server",
    "Content-Type",
    "Content-Length",
]

SECURITY_HEADERS = {
    "X-Frame-Options":
        "Protects against Clickjacking attacks.",

    "Content-Security-Policy":
        "Helps prevent Cross-Site Scripting (XSS).",

    "Strict-Transport-Security":
        "Forces browsers to use HTTPS.",

    "X-Content-Type-Options":
        "Prevents MIME type sniffing.",

    "Referrer-Policy":
        "Controls Referer header leakage."
}


def http_headers(target):

    title("HTTP Header Analysis")

    info("Connecting to target...")

    try:

        response = requests.get(
            f"https://{target}",
            timeout=10
        )

        section("General Information")

        for header in IMPORTANT_HEADERS:

            value = response.headers.get(header)

            if value:
                success(f"{header:<30}: {value}")

        section("Security Headers")

        findings = []

        for header, description in SECURITY_HEADERS.items():

            value = response.headers.get(header)

            if value:

                success(f"{header:<30}: Present")

            else:

                error(f"{header:<30}: Missing")

                findings.append((header, description))

        section("Potential Findings")

        if not findings:

            success("No missing security headers found.")

        else:

            for header, description in findings:

                warning(header)

                print(f"    Impact : {description}")

    except Exception as e:

        error(str(e))
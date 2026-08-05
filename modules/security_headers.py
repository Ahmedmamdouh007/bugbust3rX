import requests

from utils.ui import title, section, success, error, warning, info


SECURITY_HEADERS = {
    "Content-Security-Policy":
        "Helps prevent Cross-Site Scripting (XSS).",

    "Strict-Transport-Security":
        "Forces browsers to use HTTPS connections.",

    "X-Frame-Options":
        "Protects against Clickjacking attacks.",

    "X-Content-Type-Options":
        "Prevents MIME type sniffing.",

    "Referrer-Policy":
        "Controls referrer information leakage.",

    "Permissions-Policy":
        "Restricts browser features."
}


def security_headers(target):

    title("Security Headers Analysis")

    info("Collecting HTTP headers...")

    try:

        response = requests.get(
            f"https://{target}",
            timeout=10
        )

        headers = response.headers

        section("Security Headers")

        findings = []

        for header, impact in SECURITY_HEADERS.items():

            value = headers.get(header)

            if value:

                success(f"{header:<30} Present")

            else:

                error(f"{header:<30} Missing")

                findings.append((header, impact))

        section("Potential Findings")

        if not findings:

            success("All important security headers are present.")

        else:

            for header, impact in findings:

                warning(header)
                print(f"    Impact : {impact}")
                print()

    except Exception as e:

        error(str(e))
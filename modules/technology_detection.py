import requests

from utils.ui import title, section, success, error, info


def technology_detection(target):

    title("Technology Detection")

    info("Analyzing target...")

    try:

        response = requests.get(
            f"https://{target}",
            timeout=10
        )

        headers = response.headers
        html = response.text.lower()

        technologies = []

        # -----------------------------
        # Server Detection
        # -----------------------------

        server = headers.get("Server")

        if server:
            technologies.append(("Server", server))

        powered = headers.get("X-Powered-By")

        if powered:
            technologies.append(("Backend", powered))

        # -----------------------------
        # CMS Detection
        # -----------------------------

        if "wp-content" in html:
            technologies.append(("CMS", "WordPress"))

        if "drupal" in html:
            technologies.append(("CMS", "Drupal"))

        if "joomla" in html:
            technologies.append(("CMS", "Joomla"))

        # -----------------------------
        # Frontend Frameworks
        # -----------------------------

        if "bootstrap" in html:
            technologies.append(("Frontend", "Bootstrap"))

        if "jquery" in html:
            technologies.append(("Frontend", "jQuery"))

        if "react" in html:
            technologies.append(("Frontend", "React"))

        if "angular" in html:
            technologies.append(("Frontend", "Angular"))

        if "vue" in html:
            technologies.append(("Frontend", "Vue.js"))

        # -----------------------------
        # Backend Frameworks
        # -----------------------------

        if "laravel" in html:
            technologies.append(("Backend", "Laravel"))

        if "django" in html:
            technologies.append(("Backend", "Django"))

        if "asp.net" in html:
            technologies.append(("Backend", "ASP.NET"))

        if "php" in html:
            technologies.append(("Backend", "PHP"))

        section("Detected Technologies")

        if technologies:

            for category, tech in technologies:

                success(f"{category:<12} : {tech}")

        else:

            error("No technologies detected.")

    except Exception as e:

        error(str(e))
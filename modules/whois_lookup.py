import whois

from utils.ui import title, section, success, error, info


def whois_lookup(target):

    title("WHOIS Lookup")

    info("Collecting WHOIS information...")

    try:

        data = whois.whois(target)

        section("Domain Information")

        success(f"Domain          : {data.domain_name}")
        success(f"Registrar       : {data.registrar}")
        success(f"Creation Date   : {data.creation_date}")
        success(f"Expiration Date : {data.expiration_date}")
        success(f"Name Servers    : {data.name_servers}")

    except Exception as e:
        error(str(e))
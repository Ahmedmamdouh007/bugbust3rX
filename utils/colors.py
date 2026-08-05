from colorama import Fore, Style, init

init(autoreset=True)

# bugbust3rX color palette -- bright "hacker-red" theme
RED = Fore.LIGHTRED_EX + Style.BRIGHT          # primary accent / banner
GREEN = Fore.LIGHTGREEN_EX + Style.BRIGHT      # success
YELLOW = Fore.LIGHTYELLOW_EX + Style.BRIGHT    # warnings
CYAN = Fore.LIGHTCYAN_EX + Style.BRIGHT        # info / structure lines
MAGENTA = Fore.LIGHTMAGENTA_EX + Style.BRIGHT  # section titles
WHITE = Fore.LIGHTWHITE_EX + Style.BRIGHT      # prompts

RESET = Style.RESET_ALL

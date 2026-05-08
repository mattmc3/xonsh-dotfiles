from xonsh.built_ins import XSH
from config import command
from xonsh.history.main import history_main

# History backend
XSH.env["XONSH_HISTORY_BACKEND"] = "sqlite"

# Ignore commands beginning with a space.
XSH.env["HISTCONTROL"] = "ignorespace"

# Optional: explicit history file (XDG-clean)
XSH.env["XONSH_HISTORY_FILE"] = (
    __import__("pathlib").Path("~/.local/share/xonsh/xonsh-history.db").expanduser()
)

@command
def hist(args):
    n = args[0] if args else "20"

    history_main([
        "show",
        "all",
        "-n",
        "-t",
        f"-{n}:",
    ])

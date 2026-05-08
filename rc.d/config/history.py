from xonsh.built_ins import XSH

# History backend
XSH.env["XONSH_HISTORY_BACKEND"] = "sqlite"

# Ignore commands beginning with a space.
XSH.env["HISTCONTROL"] = "ignorespace"

# Optional: explicit history file (XDG-clean)
XSH.env["XONSH_HISTORY_FILE"] = (
    __import__("pathlib").Path("~/.local/share/xonsh/xonsh-history.db").expanduser()
)

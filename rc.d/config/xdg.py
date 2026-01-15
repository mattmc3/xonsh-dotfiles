from pathlib import Path
from xonsh.built_ins import XSH

defaults = {
    "XDG_CACHE_HOME": "~/.cache",
    "XDG_CONFIG_HOME": "~/.config",
    "XDG_DATA_HOME": "~/.local/share",
}

for var, default in defaults.items():
    XSH.env.setdefault(var, str(Path(default).expanduser()))
    Path(XSH.env[var]).mkdir(parents=True, exist_ok=True)

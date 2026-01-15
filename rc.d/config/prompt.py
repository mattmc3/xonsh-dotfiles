# run starship xonsh init (safe if starship isn't installed)
import subprocess
from pathlib import Path
from xonsh.built_ins import XSH

p = Path(XSH.env["HOME"]) / ".config/xonsh/themes/xonsh.toml"
if p.is_file():
    XSH.env["STARSHIP_CONFIG"] = str(p)

try:
    init_code = subprocess.check_output(
        ["starship", "init", "xonsh", "--print-full-init"],
        text=True,
        stderr=subprocess.DEVNULL,
    )
    XSH.execer.exec(init_code)
except (FileNotFoundError, subprocess.CalledProcessError):
    # starship not installed or failed; ignore silently
    pass

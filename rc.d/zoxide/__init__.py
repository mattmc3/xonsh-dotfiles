#!/usr/bin/env python
import subprocess
from xonsh.built_ins import XSH

def _init_zoxide():
    try:
        result = subprocess.run(
            ["zoxide", "init", "xonsh"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except FileNotFoundError:
        return

    if result.returncode != 0 or not result.stdout.strip():
        return

    XSH.execer.exec(result.stdout, glbs=XSH.ctx, locs=XSH.ctx, filename="zoxide")

_init_zoxide()

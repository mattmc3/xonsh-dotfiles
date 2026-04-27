#!/usr/bin/env python
import subprocess
from xonsh.built_ins import XSH
from xonsh.xontribs import xontribs_load

try:
    xontribs_load(["abbrevs"], verbose=False)
except ImportError:
    subprocess.run(["pipx", "inject", "xonsh", "xontrib-abbrevs"], check=True)
    xontribs_load(["abbrevs"], verbose=False)

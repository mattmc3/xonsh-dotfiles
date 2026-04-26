#!/usr/bin/env python
import subprocess
from xonsh.built_ins import XSH
from xonsh.xontribs import xontribs_load

try:
    xontribs_load(['abbrevs'], verbose=False)
except ImportError:
    subprocess.run(['pipx', 'inject', 'xonsh', 'xontrib-abbrevs'], check=True)
    xontribs_load(['abbrevs'], verbose=False)

abbrevs = XSH.ctx['abbrevs']

# parent directory shortcuts: ..1 -> .., ..2 -> ../.. etc.
for _i in range(1, 10):
    abbrevs[f'..{_i}'] = '/'.join(['..'] * _i)

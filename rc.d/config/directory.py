#!/usr/bin/env python
import os
import subprocess
from config import command
from xonsh.built_ins import XSH
from xonsh.events import events
from xonsh.xontribs import xontribs_load

# --- dot aliases ---

XSH.aliases['..'] = 'cd ..'

# --- dot abbreviations (..1-..9) ---

try:
    xontribs_load(['abbrevs'], verbose=False)
except ImportError:
    subprocess.run(['pipx', 'inject', 'xonsh', 'xontrib-abbrevs'], check=True)
    xontribs_load(['abbrevs'], verbose=False)

abbrevs = XSH.ctx['abbrevs']

# standalone: ..2 -> cd ../..   as argument: ls ..2 -> ls ../..
for _i in range(1, 10):
    _path = '/'.join(['..'] * _i)
    abbrevs[f'..{_i}'] = lambda buffer, word, p=_path: f'cd {p}' if buffer.text.strip() == word else p

# --- directory history (dirh / d..N) ---

_dir_history = []

@events.on_chdir
def _track_dirs(olddir, newdir, **kwargs):
    if olddir and olddir != newdir:
        if not _dir_history or _dir_history[0] != olddir:
            _dir_history.insert(0, olddir)
            del _dir_history[20:]


def _fmt_dir(path):
    home = XSH.env.get('HOME', '')
    if home and path.startswith(home):
        return '~' + path[len(home):]
    return path


@command
def dirh(args):
    print(f' 0  {_fmt_dir(os.getcwd())}')
    for i, d in enumerate(_dir_history, 1):
        print(f'{i:2}  {_fmt_dir(d)}')


def _make_cd_history(n):
    def _go(args):
        if n <= len(_dir_history):
            os.chdir(_dir_history[n - 1])
        else:
            print(f'dirh: no such entry: {n}')
    return _go

for _i in range(1, 10):
    XSH.aliases[f'd..{_i}'] = _make_cd_history(_i)

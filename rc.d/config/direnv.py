#!/usr/bin/env python
import json
import shutil
import subprocess
from pathlib import Path
from xonsh.built_ins import XSH
from xonsh.events import events

if shutil.which('direnv'):
    def _direnv():
        result = subprocess.run(
            ['direnv', 'export', 'json'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        if not result.stdout.strip():
            return
        with XSH.env.swap(UPDATE_OS_ENVIRON=True):
            for k, v in json.loads(result.stdout).items():
                if v is None:
                    del XSH.env[k]
                else:
                    XSH.env[k] = v

    @events.on_post_init
    def _direnv_post_init(**kwargs):
        _direnv()

    @events.on_chdir
    def _direnv_chdir(olddir, newdir, **kwargs):
        direnv_dir = XSH.env.get('DIRENV_DIR')
        if direnv_dir is not None:
            direnv_path = Path(direnv_dir.lstrip('-'))
            if not set(direnv_path.parts).issubset(Path(newdir).absolute().parts):
                _direnv()
        else:
            _direnv()

    @events.on_postcommand
    def _direnv_postcommand(cmd, rtn, out, ts, **kwargs):
        _direnv()

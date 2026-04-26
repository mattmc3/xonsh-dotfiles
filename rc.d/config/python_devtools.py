#!/usr/bin/env python
import shutil
import subprocess
import sys
from pathlib import Path
from xonsh.built_ins import XSH
from xonsh.completers.tools import contextual_command_completer, RichCompletion


def _workon_home():
    xdg_data = XSH.env.get('XDG_DATA_HOME', str(Path.home() / '.local' / 'share'))
    return Path(XSH.env.get('WORKON_HOME', Path(xdg_data) / 'venvs'))


def _activate(venv_path):
    venv_path = Path(venv_path)
    venv_bin = str(venv_path / 'bin')
    XSH.env['VIRTUAL_ENV'] = str(venv_path)
    XSH.env['PATH'] = [venv_bin] + [p for p in XSH.env['PATH'] if p != venv_bin]
    XSH.env.pop('PYTHONHOME', None)


def _list_venvs():
    workon_home = _workon_home()
    if not workon_home.exists():
        return set()
    return {d.name for d in workon_home.iterdir()
            if d.is_dir() and (d / 'bin' / 'activate').exists()}


def venv_(args):
    workon_home = _workon_home()

    if not args:
        print("usage: venv create|workon|home|list|remove ...", file=sys.stderr)
        return 1

    cmd, *rest = args

    if cmd == 'create':
        if not rest:
            print("venv create: expected <name>", file=sys.stderr)
            return 1
        venv_path = workon_home / rest[0]
        if venv_path.exists():
            print(f"venv: already exists: '{rest[0]}'", file=sys.stderr)
            return 1
        subprocess.run(['python3', '-m', 'venv', str(venv_path)], check=True)

    elif cmd == 'list':
        workon_home.mkdir(parents=True, exist_ok=True)
        for d in sorted(workon_home.iterdir()):
            if d.is_dir() and (d / 'bin' / 'activate').exists():
                print(d.name)

    elif cmd == 'home':
        if rest:
            venv_path = workon_home / rest[0]
            if not venv_path.exists():
                print(f"venv: not found: '{rest[0]}'", file=sys.stderr)
                return 1
            print(str(venv_path))
        else:
            print(str(workon_home))

    elif cmd == 'workon':
        if not rest:
            print("venv workon: expected <name>", file=sys.stderr)
            return 1
        venv_path = workon_home / rest[0]
        if not venv_path.exists():
            subprocess.run(['python3', '-m', 'venv', str(venv_path)], check=True)
        _activate(venv_path)

    elif cmd == 'remove':
        if not rest:
            print("venv remove: expected <name>", file=sys.stderr)
            return 1
        venv_path = workon_home / rest[0]
        if not venv_path.exists():
            print(f"venv: not found: '{rest[0]}'", file=sys.stderr)
            return 1
        shutil.rmtree(venv_path)

    else:
        print(f"venv: unknown subcommand '{cmd}'", file=sys.stderr)
        return 1


def workon_(args):
    venv_(['workon'] + list(args))


def juno_(args):
    workon_home = _workon_home()
    juno_venv = workon_home / 'juno'

    if not juno_venv.exists():
        subprocess.run(['python3', '-m', 'venv', str(juno_venv)], check=True)
        pip = str(juno_venv / 'bin' / 'pip')
        subprocess.run([pip, 'install', '--upgrade', 'pip'], check=True)
        subprocess.run([pip, 'install', 'jupyterlab', 'pandas'], check=True)

    jupyter_prj = Path.home() / 'Projects' / 'mattmc3' / 'jupyter'
    if not jupyter_prj.exists():
        subprocess.run(['git', 'clone', 'git@github.com:mattmc3/jupyter', str(jupyter_prj)], check=True)

    jupyter = str(juno_venv / 'bin' / 'jupyter')
    subprocess.run([jupyter, 'lab', args[0] if args else str(jupyter_prj)])


@contextual_command_completer
def _venv_completer(context):
    if not context.args or context.args[0].value != 'venv':
        return
    prefix = context.prefix
    if context.arg_index == 1:
        return {RichCompletion(c, append_space=True) for c in {'create', 'home', 'list', 'remove', 'workon'} if c.startswith(prefix)}
    if context.arg_index == 2 and len(context.args) > 1:
        if context.args[1].value in ('home', 'remove', 'workon'):
            return {c for c in _list_venvs() if c.startswith(prefix)}
        return set()


@contextual_command_completer
def _workon_completer(context):
    if not context.args or context.args[0].value != 'workon':
        return
    if context.arg_index == 1:
        return {c for c in _list_venvs() if c.startswith(context.prefix)}


XSH.aliases['venv'] = venv_
XSH.aliases['workon'] = workon_
XSH.aliases['juno'] = juno_
old = dict(XSH.completers)
XSH.completers.clear()
XSH.completers['venv'] = _venv_completer
XSH.completers['workon'] = _workon_completer
XSH.completers.update(old)

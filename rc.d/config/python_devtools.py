#!/usr/bin/env python
import shutil
import subprocess
import sys
from pathlib import Path
from xonsh.built_ins import XSH
from xonsh.completers.completer import add_one_completer
from xonsh.completers.tools import contextual_command_completer_for, RichCompletion

# Notes:
#  - consider using xontrib-vox

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


def deactivate_(_):
    venv = XSH.env.get('VIRTUAL_ENV')
    if not venv:
        print("deactivate: no active virtual environment", file=sys.stderr)
        return 1
    venv_bin = str(Path(venv) / 'bin')
    XSH.env['PATH'] = [p for p in XSH.env['PATH'] if p != venv_bin]
    del XSH.env['VIRTUAL_ENV']


def pyclean_(args):
    roots = [Path(a) for a in args] if args else [Path('.')]
    for root in roots:
        for p in root.rglob('*.pyc'):
            p.unlink()
        for p in root.rglob('*.pyo'):
            p.unlink()
        for d in root.rglob('__pycache__'):
            if d.is_dir():
                shutil.rmtree(d)
        for d in root.rglob('.mypy_cache'):
            if d.is_dir():
                shutil.rmtree(d)
        for d in root.rglob('.pytest_cache'):
            if d.is_dir():
                shutil.rmtree(d)


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


@contextual_command_completer_for('venv')
def _venv_completer(command):
    prefix = command.prefix
    if command.arg_index == 1:
        return {RichCompletion(c, append_space=True) for c in {'create', 'home', 'list', 'remove', 'workon'} if c.startswith(prefix)}
    if command.arg_index == 2 and len(command.args) > 1:
        if command.args[1].value in ('home', 'remove', 'workon'):
            return {c for c in _list_venvs() if c.startswith(prefix)}
        return set()


@contextual_command_completer_for('workon')
def _workon_completer(command):
    if command.arg_index == 1:
        return {c for c in _list_venvs() if c.startswith(command.prefix)}


XSH.aliases['venv'] = venv_
XSH.aliases['workon'] = workon_
XSH.aliases['deactivate'] = deactivate_
XSH.aliases['juno'] = juno_
XSH.aliases['pyclean'] = pyclean_
add_one_completer('venv', _venv_completer, 'start')
add_one_completer('workon', _workon_completer, 'start')

if not shutil.which('python') and shutil.which('python3'):
    XSH.aliases['python'] = 'python3'
if not shutil.which('pip') and shutil.which('pip3'):
    XSH.aliases['pip'] = 'pip3'

#!/usr/bin/env python
import os
import subprocess
import sys
from pathlib import Path
from config import command
from xonsh.built_ins import XSH

XSH.aliases['brewup'] = 'brew update && brew upgrade && brew cleanup'
XSH.aliases['brewinfo'] = 'brew leaves | xargs brew desc --eval-all'
XSH.aliases['flushdns'] = 'dscacheutil -flushcache && sudo killall -HUP mDNSResponder'
XSH.aliases['hidefiles'] = 'defaults write com.apple.finder AppleShowAllFiles -bool false && killall Finder'
XSH.aliases['showfiles'] = 'defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder'


def _pfd():
    """Return the frontmost Finder directory as a string."""
    result = subprocess.run(
        ['osascript', '-e', 'tell application "Finder" to return POSIX path of (target of first window as text)'],
        capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


@command
def pfd(_):
    """Print the frontmost Finder directory."""
    path = _pfd()
    if path:
        print(path)


@command
def pfs(_):
    """Print the current Finder selection."""
    result = subprocess.run(
        ['osascript', '-e', '''
            tell application "Finder" to set the_selection to selection
            if the_selection is not {}
                repeat with an_item in the_selection
                    log POSIX path of (an_item as text)
                end repeat
            end if
        '''],
        capture_output=True, text=True,
    )
    if result.stderr.strip():
        print(result.stderr.strip())


@command
def cdf(_):
    """Change to the current Finder directory."""
    path = _pfd()
    if path:
        os.chdir(path)


@command
def ofd(_):
    """Open the current directory in Finder."""
    subprocess.run(['open', os.getcwd()])


@command
def pushdf(_):
    """Push the current Finder directory onto the dir stack."""
    path = _pfd()
    if path:
        os.chdir(path)


@command
def peek(args):
    """Quick look at a file."""
    if not args:
        print("peek: expected <file>", file=sys.stderr)
        return 1
    subprocess.Popen(['qlmanage', '-p'] + list(args),
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@command
def lmk(args):
    """Say a message (or 'Process complete.') via Siri."""
    subprocess.run(['say', ' '.join(args) if args else 'Process complete.'])


@command
def manp(args):
    """Read a man page in Preview.app."""
    if not args:
        print("manp: expected <page>", file=sys.stderr)
        return 1
    man = subprocess.run(['man', '-w'] + list(args), capture_output=True, text=True)
    if man.returncode != 0:
        return man.returncode
    pdf = subprocess.run(['mandoc', '-T', 'pdf', man.stdout.strip()], capture_output=True)
    subprocess.run(['open', '-fa', 'Preview'], input=pdf.stdout)


@command
def mand(args):
    """Read a man page in Dash.app."""
    if not args:
        print("mand: expected <page>", file=sys.stderr)
        return 1
    result = subprocess.run(['open', '-a', 'Dash.app', f'dash://manpages%3A{args[-1]}'],
                            capture_output=True)
    if result.returncode != 0:
        print("mand: Dash is not installed", file=sys.stderr)
        return 2


@command
def trash(args):
    """Move files to the macOS trash."""
    if not args:
        print("trash: usage: trash <files...>", file=sys.stderr)
        return 64
    items = []
    for f in args:
        p = Path(f)
        if p.is_symlink():
            print(f"trash: cannot move symlink to trash: '{f}'", file=sys.stderr)
        elif p.exists():
            items.append(f'the POSIX file "{p.absolute()}"')
        else:
            print(f"trash: no such file or directory: '{f}'", file=sys.stderr)
            return 1
    if items:
        subprocess.run(['osascript', '-e',
                        f'tell app "Finder" to move {{{", ".join(items)}}} to trash'])


def del_(args):
    """Safe delete — moves to trash."""
    trash(args)
XSH.aliases['del'] = del_


@command
def rmdsstore(args):
    """Recursively remove .DS_Store files."""
    roots = [Path(a) for a in args] if args else [Path('.')]
    for root in roots:
        for p in root.rglob('.DS_Store'):
            p.unlink()

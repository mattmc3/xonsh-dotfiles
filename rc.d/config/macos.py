#!/usr/bin/env python
import os
import subprocess
import sys
from pathlib import Path
from xonsh.built_ins import XSH

XSH.aliases['brewup'] = 'brew update && brew upgrade && brew cleanup'
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


def pfd_(_):
    """Print the frontmost Finder directory."""
    path = _pfd()
    if path:
        print(path)
XSH.aliases['pfd'] = pfd_


def pfs_(_):
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
XSH.aliases['pfs'] = pfs_


def cdf_(_):
    """Change to the current Finder directory."""
    path = _pfd()
    if path:
        os.chdir(path)
XSH.aliases['cdf'] = cdf_


def ofd_(_):
    """Open the current directory in Finder."""
    subprocess.run(['open', os.getcwd()])
XSH.aliases['ofd'] = ofd_


def pushdf_(_):
    """Push the current Finder directory onto the dir stack."""
    path = _pfd()
    if path:
        os.chdir(path)
XSH.aliases['pushdf'] = pushdf_


def peek_(args):
    """Quick look at a file."""
    if not args:
        print("peek: expected <file>", file=sys.stderr)
        return 1
    subprocess.Popen(['qlmanage', '-p'] + list(args),
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
XSH.aliases['peek'] = peek_


def lmk_(args):
    """Say a message (or 'Process complete.') via Siri."""
    subprocess.run(['say', ' '.join(args) if args else 'Process complete.'])
XSH.aliases['lmk'] = lmk_


def manp_(args):
    """Read a man page in Preview.app."""
    if not args:
        print("manp: expected <page>", file=sys.stderr)
        return 1
    man = subprocess.run(['man', '-w'] + list(args), capture_output=True, text=True)
    if man.returncode != 0:
        return man.returncode
    pdf = subprocess.run(['mandoc', '-T', 'pdf', man.stdout.strip()], capture_output=True)
    subprocess.run(['open', '-fa', 'Preview'], input=pdf.stdout)
XSH.aliases['manp'] = manp_


def mand_(args):
    """Read a man page in Dash.app."""
    if not args:
        print("mand: expected <page>", file=sys.stderr)
        return 1
    result = subprocess.run(['open', '-a', 'Dash.app', f'dash://manpages%3A{args[-1]}'],
                            capture_output=True)
    if result.returncode != 0:
        print("mand: Dash is not installed", file=sys.stderr)
        return 2
XSH.aliases['mand'] = mand_


def trash_(args):
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
XSH.aliases['trash'] = trash_


def del_(args):
    """Safe delete — moves to trash."""
    trash_(args)
XSH.aliases['del'] = del_


def rmdsstore_(args):
    """Recursively remove .DS_Store files."""
    roots = [Path(a) for a in args] if args else [Path('.')]
    for root in roots:
        for p in root.rglob('.DS_Store'):
            p.unlink()
XSH.aliases['rmdsstore'] = rmdsstore_

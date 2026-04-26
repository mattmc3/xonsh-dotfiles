#!/usr/bin/env python
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from xonsh.built_ins import XSH


class Clipboard:
    def __init__(self):
        self._copy = None  # callable(data: bytes)
        self._paste = None  # callable()

    def _detect(self):
        """Detect clipboard provider, set copy/paste callables and $CLIPBOARD_APP."""
        os_type = platform.system()

        if os_type == 'Darwin' and shutil.which('pbcopy'):
            XSH.env['CLIPBOARD_APP'] = 'pbcopy'
            self._copy  = lambda data: subprocess.run(['pbcopy'], input=data)
            self._paste = lambda: subprocess.run(['pbpaste'])

        elif shutil.which('clip.exe') and shutil.which('powershell.exe'):
            XSH.env['CLIPBOARD_APP'] = 'clip.exe'
            self._copy  = lambda data: subprocess.run(['clip.exe'], input=data)
            self._paste = lambda: subprocess.run(['powershell.exe', '-noprofile', '-command', 'Get-Clipboard'])

        elif XSH.env.get('WAYLAND_DISPLAY') and shutil.which('wl-copy'):
            XSH.env['CLIPBOARD_APP'] = 'wl-copy'
            self._copy  = lambda data: subprocess.run(['wl-copy'], input=data)
            self._paste = lambda: subprocess.run(['wl-paste', '--no-newline'])

        elif XSH.env.get('DISPLAY') and shutil.which('xsel'):
            XSH.env['CLIPBOARD_APP'] = 'xsel'
            self._copy  = lambda data: subprocess.run(['xsel', '--clipboard', '--input'], input=data)
            self._paste = lambda: subprocess.run(['xsel', '--clipboard', '--output'])

        elif XSH.env.get('DISPLAY') and shutil.which('xclip'):
            XSH.env['CLIPBOARD_APP'] = 'xclip'
            self._copy  = lambda data: subprocess.run(['xclip', '-selection', 'clipboard', '-in'], input=data)
            self._paste = lambda: subprocess.run(['xclip', '-out', '-selection', 'clipboard'])

        elif shutil.which('lemonade'):
            XSH.env['CLIPBOARD_APP'] = 'lemonade'
            self._copy  = lambda data: subprocess.run(['lemonade', 'copy'], input=data)
            self._paste = lambda: subprocess.run(['lemonade', 'paste'])

        elif shutil.which('doitclient'):
            XSH.env['CLIPBOARD_APP'] = 'doitclient'
            self._copy  = lambda data: subprocess.run(['doitclient', 'wclip'], input=data)
            self._paste = lambda: subprocess.run(['doitclient', 'wclip', '-r'])

        elif shutil.which('win32yank'):
            XSH.env['CLIPBOARD_APP'] = 'win32yank'
            self._copy  = lambda data: subprocess.run(['win32yank', '-i'], input=data)
            self._paste = lambda: subprocess.run(['win32yank', '-o'])

        elif os_type == 'Linux' and shutil.which('termux-clipboard-set'):
            XSH.env['CLIPBOARD_APP'] = 'termux-clipboard-set'
            self._copy  = lambda data: subprocess.run(['termux-clipboard-set'], input=data)
            self._paste = lambda: subprocess.run(['termux-clipboard-get'])

        elif XSH.env.get('TMUX') and shutil.which('tmux'):
            XSH.env['CLIPBOARD_APP'] = 'tmux'
            self._copy  = lambda data: subprocess.run(['tmux', 'load-buffer', '-w', '-'], input=data)
            self._paste = lambda: subprocess.run(['tmux', 'save-buffer', '-'])

        else:
            raise RuntimeError("no clipboard provider found")

    def _ensure(self):
        if self._copy is None:
            self._detect()

    def copy(self, args, stdin=None):
        """Copy data to clipboard from stdin or file."""
        self._ensure()
        if args:
            data = open(args[0], 'rb').read()
        else:
            src = stdin or sys.stdin
            data = src.buffer.read() if hasattr(src, 'buffer') else src.read()
            if isinstance(data, str):
                data = data.encode()
        self._copy(data)

    def paste(self, _):
        """Paste clipboard contents to stdout."""
        self._ensure()
        self._paste()

    def copyfile(self, args):
        """Copy a file's contents to the clipboard."""
        if not args:
            print("copyfile: usage: copyfile <file>", file=sys.stderr)
            return 1
        f = args[0]
        if not os.path.isfile(f):
            print(f"copyfile: '{f}' is not a valid file", file=sys.stderr)
            return 1
        self._ensure()
        self._copy(open(f, 'rb').read())
        print(f"{f} copied to clipboard.")

    def copypath(self, args):
        """Copy the absolute path of a file or directory to the clipboard."""
        path = Path(args[0] if args else '.').absolute()
        self._ensure()
        self._copy(str(path).encode())
        print(f"{path} copied to clipboard.")


_clipboard = Clipboard()
XSH.aliases['clipcopy'] = _clipboard.copy
XSH.aliases['clippaste'] = _clipboard.paste
XSH.aliases['copyfile'] = _clipboard.copyfile
XSH.aliases['copypath'] = _clipboard.copypath

#!/usr/bin/env python
import sys
from pathlib import Path

import pyperclip
from config import command
from xonsh.events import events


@command
def clipcopy(args, stdin=None):
    """Copy data to clipboard from stdin or file."""
    if args:
        data = open(args[0]).read()
    else:
        src = stdin or sys.stdin
        data = src.read()
    pyperclip.copy(data)


@command
def clippaste(_):
    """Paste clipboard contents to stdout."""
    print(pyperclip.paste(), end='')


@command
def copyfile(args):
    """Copy a file's contents to the clipboard."""
    if not args:
        print("copyfile: usage: copyfile <file>", file=sys.stderr)
        return 1
    f = args[0]
    if not Path(f).is_file():
        print(f"copyfile: '{f}' is not a valid file", file=sys.stderr)
        return 1
    pyperclip.copy(open(f).read())
    print(f"{f} copied to clipboard.")


@command
def copypath(args):
    """Copy the absolute path of a file or directory to the clipboard."""
    path = Path(args[0] if args else '.').absolute()
    pyperclip.copy(str(path))
    print(f"{path} copied to clipboard.")


@events.on_ptk_create
def _setup_copybuffer(bindings, **kwargs):
    @bindings.add('c-o')
    def copybuffer(event):
        text = event.app.current_buffer.text
        if text:
            pyperclip.copy(text)

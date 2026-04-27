import os
import subprocess
from config import command


@command
def up(args):
    """Go up any number of directories"""
    n = int(args[0]) if args else 1
    os.chdir("../" * n)


@command
def sedi(args):
    """Cross-platform sed -i (detects GNU vs BSD)"""
    is_gnu = subprocess.run(["sed", "--version"], capture_output=True).returncode == 0
    if is_gnu:
        subprocess.run(["sed", "-i", "--"] + list(args))
    else:
        subprocess.run(["sed", "-i", ""] + list(args))


@command
def colormap(_):
    """Show terminal 256-color colormap"""
    for i in range(256):
        print(f"\x1b[48;5;{i}m  \x1b[0m\x1b[38;5;{i}m{i:03d}\x1b[0m", end=" ")
        if i % 6 == 3:
            print()

#!/usr/bin/env python
import platform
import config
from nu import *

config.load(
    "xdg",
    "environment",
    "abbrevs",
    "aliases",
    "azure",
    "clipboard",
    "describe",
    "direnv",
    "git",
    "dirstack",
    "history",
    "iwd",
    "magic_enter",
    "prompt",
    "python_devtools",
    "symmetric_ctrl_z",
    "utils",
    "zoxide",
)

if platform.system() == 'Darwin':
    config.load("macos")

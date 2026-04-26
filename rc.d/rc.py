#!/usr/bin/env python
import config
from nu import *

config.load(
    "xdg",
    "environment",
    "abbrevs",
    "aliases",
    "direnv",
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

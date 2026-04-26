#!/usr/bin/env python
import config
from nu import *

config.load(
    "xdg",
    "environment",
    "aliases",
    "history",
    "iwd",
    "magic_enter",
    "prompt",
    "symmetric_ctrl_z",
    "utils",
    "zoxide",
)

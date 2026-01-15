#!/usr/bin/env python
import config
from nu import *

config.load(
    "xdg",
    "environment",
    "aliases",
    "history",
    "magic_enter",
    "prompt",
    "utils",
    "zoxide",
)

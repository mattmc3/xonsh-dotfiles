#!/usr/bin/env python
import platform
import config
from nu import *
from xonsh.xontribs import xontribs_load
from xonsh.built_ins import XSH

config.load(
    "xdg",
    "environment",
    "abbrevs",
    "aliases",
    "azure",
    "clipboard",
    "describe",
    "direnv",
    "directory",
    "fzf_widgets",
    "git",
    "history",
    "iwd",
    "magic_enter",
    "prompt",
    "python_devtools",
    "symmetric_ctrl_z",
    "utils",
    "zoxide",
)

if platform.system() == "Darwin":
    config.load("macos")

XSH.env["fzf_history_binding"] = "up"
XSH.env["fzf_ssh_binding"] = None
XSH.env["fzf_file_binding"] = None
XSH.env["fzf_dir_binding"] = None

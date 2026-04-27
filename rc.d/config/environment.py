#!/usr/bin/env python
# https://xon.sh/envvars.html
import platform
from xonsh.built_ins import XSH

XSH.env["EDITOR"] = "nvim"
XSH.env["VISUAL"] = "code"
XSH.env["PAGER"] = "less"
XSH.env["LANG"] = "en_US.UTF-8"
XSH.env["XONSH_PROMPT_CURSOR_SHAPE"] = "beam"

XSH.env["LESS"] = "-g -i -M -R -S -w -z-4"
XSH.env["LESS_TERMCAP_mb"] = "\033[1;34m"  # bold blue  (blink start)
XSH.env["LESS_TERMCAP_md"] = "\033[1;36m"  # bold cyan  (bold start)
XSH.env["LESS_TERMCAP_me"] = "\033[0m"  # reset
XSH.env["LESS_TERMCAP_so"] = "\033[30;47m"  # black on white (standout)
XSH.env["LESS_TERMCAP_se"] = "\033[0m"  # reset
XSH.env["LESS_TERMCAP_us"] = "\033[1;35m"  # bold magenta (underline start)
XSH.env["LESS_TERMCAP_ue"] = "\033[0m"  # reset

LS_COLORS = (
    "di=34:ln=35:so=32:pi=33:ex=31:bd=1;36:cd=1;33:su=30;41:sg=30;46:tw=30;42:ow=30;43"
)
XSH.env["LS_COLORS"] = LS_COLORS
XSH.env["EZA_COLORS"] = (
    f"{LS_COLORS}:or=1;31:fi=0:da=2:sn=33:sb=2:uu=33:un=2:gu=35:gn=2:lp=35:ur=33:uw=31:ux=32:ue=32:gr=2;33:gw=2;31:gx=2;32:tr=2:tx=2:xa=2"
)

if platform.system() == "Darwin":
    XSH.env["SHELL_SESSIONS_DISABLE"] = "1"
    XSH.env["BROWSER"] = "open"

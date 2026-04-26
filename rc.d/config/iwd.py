#!/usr/bin/env python
import os
from xonsh.built_ins import XSH

def _init_iwd():
    XSH.env["IWD"] = XSH.env.get("PWD", os.getcwd())

    def _iwd(args, stdin=None):
        os.chdir(XSH.env["IWD"])

    XSH.aliases["iwd"] = _iwd

_init_iwd()

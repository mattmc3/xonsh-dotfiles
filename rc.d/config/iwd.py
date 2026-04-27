#!/usr/bin/env python
import os
from config import command
from xonsh.built_ins import XSH

XSH.env["IWD"] = XSH.env.get("PWD", os.getcwd())


@command
def iwd(args, stdin=None):
    os.chdir(XSH.env["IWD"])

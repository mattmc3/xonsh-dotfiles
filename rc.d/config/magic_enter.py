#!/usr/bin/env python
import subprocess
from pathlib import Path
from xonsh.built_ins import XSH
from xonsh.events import events

XSH.env["MAGIC_ENTER_GIT_COMMAND"] = ["git", "status", "-sb", "."]
XSH.env["MAGIC_ENTER_OTHER_COMMAND"] = ["ls", "-lahF", "."]
XSH.env["MAGIC_ENTER_RUN_COMMAND"] = None

@events.on_transform_command
def magic_enter(cmd, **_):
    """Run a command when Enter is pressed on an empty line."""
    if not cmd.strip():
        pwd = Path(XSH.env["PWD"])
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=str(pwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip() == "true":
            XSH.env["MAGIC_ENTER_RUN_COMMAND"] = XSH.env["MAGIC_ENTER_GIT_COMMAND"]
        else:
            XSH.env["MAGIC_ENTER_RUN_COMMAND"] = XSH.env["MAGIC_ENTER_OTHER_COMMAND"]
    return cmd

@events.on_pre_prompt
def run_magic_enter():
    cmd = XSH.env.get("MAGIC_ENTER_RUN_COMMAND")
    if cmd:
        XSH.subproc_uncaptured(cmd)
    XSH.env["MAGIC_ENTER_RUN_COMMAND"] = None

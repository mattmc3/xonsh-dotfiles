#!/usr/bin/env python
import subprocess
from pathlib import Path
from xonsh.built_ins import XSH
from xonsh.events import events

# ---- config ----
env = XSH.env
env["MAGIC_ENTER_GIT_COMMAND"] = ["git", "status", "-sb", "."]
env["MAGIC_ENTER_OTHER_COMMAND"] = ["ls", "-lahF", "."]
env["MAGIC_ENTER_RUN_COMMAND"] = None


# ---- hooks ----

@events.on_transform_command
def magic_enter(cmd, **_):
    """Run a command when Enter is pressed on an empty line."""
    if not cmd.strip():
        pwd = Path(env["PWD"])
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=str(pwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip() == "true":
            env["MAGIC_ENTER_RUN_COMMAND"] = env["MAGIC_ENTER_GIT_COMMAND"]
        else:
            env["MAGIC_ENTER_RUN_COMMAND"] = env["MAGIC_ENTER_OTHER_COMMAND"]
    return cmd


@events.on_pre_prompt
def run_magic_enter():
    cmd = env.get("MAGIC_ENTER_RUN_COMMAND")
    if cmd:
        XSH.subproc_uncaptured(cmd)
    env["MAGIC_ENTER_RUN_COMMAND"] = None

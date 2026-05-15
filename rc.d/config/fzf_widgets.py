import os
import re
import shutil
import subprocess
from io import StringIO

from prompt_toolkit.keys import Keys
from xonsh.built_ins import XSH
from xonsh.completers.path import complete_path
from xonsh.events import events
from xonsh.history.main import history_main


def envget(name, default=None):
    return XSH.env.get(name, default)


def get_fzf_binary_name():
    if "TMUX" in os.environ and shutil.which("fzf-tmux"):
        return "fzf-tmux"
    return "fzf"


def get_fzf_binary_path():
    path = shutil.which(get_fzf_binary_name())
    if not path:
        raise RuntimeError(
            "Could not find fzf. Install it and make sure it is on PATH."
        )
    return path


def uniq(items):
    seen = set()
    for item in items:
        if item and item not in seen:
            seen.add(item)
            yield item


def write_deduped_history(stdout):
    raw = StringIO()
    history_main(args=["show", "-0", "all"], stdout=raw)

    for cmd in uniq(raw.getvalue().split("\0")):
        stdout.write(cmd)
        stdout.write("\0")


def fzf_insert_history(event):
    popen_args = [
        get_fzf_binary_path(),
        "--read0",
        "--tac",
        "--cycle",
        "--tiebreak=index",
        "+m",
        "--reverse",
        "--height=40%",
        "--bind=ctrl-r:toggle-sort",
    ]
    # popen_args = [
    #     get_fzf_binary_path(),
    #     "--read0",
    #     "--no-sort",
    #     "--cycle",
    #     "+m",
    #     "--reverse",
    #     "--height=40%",
    #     "--bind=start:last",
    # ]

    query = event.current_buffer.text
    if query:
        popen_args.extend(["--query", query])

    proc = subprocess.Popen(
        popen_args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )

    write_deduped_history(proc.stdin)
    proc.stdin.close()
    proc.wait()

    choice = proc.stdout.read().strip()

    event.cli.renderer.erase()

    if choice:
        event.current_buffer.text = choice
        event.current_buffer.cursor_position = len(choice)


def fzf_insert_file(event, dirs_only=False):
    before_cursor = event.current_buffer.document.current_line_before_cursor
    delim_pos = before_cursor.rfind(" ", 0, len(before_cursor))

    prefix = None
    if delim_pos != -1 and delim_pos != len(before_cursor) - 1:
        prefix = before_cursor[delim_pos + 1 :]

    cwd = None
    path = ""

    if prefix:
        paths = complete_path(
            os.path.normpath(prefix),
            before_cursor,
            0,
            len(before_cursor),
            None,
        )[0]

        if len(paths) == 1:
            path = paths.pop()

    expanded_path = os.path.expanduser(path)

    if os.path.isdir(expanded_path):
        cwd = os.getcwd()
        os.chdir(expanded_path)

    env = os.environ.copy()

    if dirs_only:
        find_dirs_command = envget("fzf_find_dirs_command")
        if find_dirs_command:
            env["FZF_DEFAULT_COMMAND"] = find_dirs_command
    else:
        find_command = envget("fzf_find_command")
        if find_command:
            env["FZF_DEFAULT_COMMAND"] = find_command

    default_opts = envget("FZF_DEFAULT_OPTS")
    if default_opts:
        env["FZF_DEFAULT_OPTS"] = default_opts

    choice = subprocess.run(
        [get_fzf_binary_path(), "-m", "--reverse", "--height=40%"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
        env=env,
    ).stdout.strip()

    if cwd:
        os.chdir(cwd)

    event.cli.renderer.erase()

    if choice:
        if path:
            event.current_buffer.delete_before_cursor(len(prefix))

        command = ""
        for c in choice.splitlines():
            command += "'" + os.path.join(path, c.strip()) + "' "

        event.current_buffer.insert_text(command.strip())


def fzf_prompt_from_string(string):
    return subprocess.run(
        [
            get_fzf_binary_path(),
            "--tiebreak=index",
            "+m",
            "--reverse",
            "--height=40%",
        ],
        input=string,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    ).stdout.strip()


def read_ssh_hosts():
    chunks = []

    for filename in (
        os.path.expanduser("~/.ssh/config"),
        "/etc/ssh/ssh_config",
    ):
        try:
            with open(filename, encoding="utf-8") as f:
                chunks.append(f.read())
        except OSError:
            pass

    return "\n".join(chunks)


@events.on_ptk_create
def custom_keybindings(bindings, **kw):
    def handler(env_name):
        key_name = envget(env_name)

        def do_nothing(func):
            return func

        if not key_name:
            return do_nothing

        key = getattr(Keys, key_name, None)

        if key is None and isinstance(key_name, str):
            # prompt_toolkit accepts strings like "c-r", "up", etc.
            key = key_name

        return bindings.add(key)

    @handler("fzf_history_binding")
    def fzf_history(event):
        fzf_insert_history(event)

    @handler("fzf_ssh_binding")
    def fzf_ssh(event):
        items = "\n".join(
            re.findall(
                r"Host\s(.*)\n?",
                read_ssh_hosts(),
                re.IGNORECASE,
            )
        )

        choice = fzf_prompt_from_string(items)

        event.cli.renderer.erase()

        if choice:
            event.current_buffer.insert_text("ssh " + choice)

    @handler("fzf_file_binding")
    def fzf_file(event):
        fzf_insert_file(event)

    @handler("fzf_dir_binding")
    def fzf_dir(event):
        fzf_insert_file(event, True)


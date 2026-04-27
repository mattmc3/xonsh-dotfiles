#!/usr/bin/env python
import inspect
import re
import sqlite3
import sys
from config import command
from xonsh.built_ins import XSH


def _from_history(name):
    """Search xonsh SQLite history for the most recent definition of name in this session."""
    if XSH.env.get('XONSH_HISTORY_BACKEND', '').lower() != 'sqlite':
        return None

    hist = getattr(XSH, 'history', None)
    filename = (
        XSH.env.get('XONSH_HISTORY_FILE')
        or getattr(hist, 'filename', None)
    )
    if not filename:
        return None

    start_time = getattr(hist, 'start_time', None)
    conn = None
    try:
        conn = sqlite3.connect(str(filename))
        if start_time:
            cursor = conn.execute(
                "SELECT inp FROM xonsh_history WHERE inp LIKE ? AND tsb >= ? ORDER BY tsb DESC LIMIT 20",
                (f'def {name}%', start_time)
            )
        else:
            cursor = conn.execute(
                "SELECT inp FROM xonsh_history WHERE inp LIKE ? ORDER BY tsb DESC LIMIT 20",
                (f'def {name}%',)
            )
        for (inp,) in cursor:
            if re.match(rf'\s*def\s+{re.escape(name)}\s*\(', inp):
                return inp.strip()
    except Exception:
        pass
    finally:
        if conn:
            conn.close()
    return None


@command
def describe(args):
    """Print the source of a named alias or function"""
    if not args:
        print("describe: expected <name>", file=sys.stderr)
        return 1
    name = args[0]
    fn = XSH.aliases.get(name) or XSH.ctx.get(name)
    if fn is None:
        for mod in sys.modules.values():
            candidate = getattr(mod, name, None)
            if callable(candidate):
                fn = candidate
                break
    if fn is None:
        print(f"describe: not found: '{name}'", file=sys.stderr)
        return 1
    if isinstance(fn, list):
        fn = next((f for f in fn if callable(f)), None)
    if fn is None or not callable(fn):
        print(f"describe: '{name}' is not a function", file=sys.stderr)
        return 1
    fn = getattr(fn, 'func', fn)
    try:
        print(inspect.getsource(fn))
    except OSError:
        src = _from_history(name)
        if src:
            print(src)
        else:
            print(f"describe: source not available for '{name}'", file=sys.stderr)
            return 1

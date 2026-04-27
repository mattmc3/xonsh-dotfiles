#!/usr/bin/env python
import inspect
import json
import re
import sqlite3
import sys

from config import command
from xonsh.built_ins import XSH


def _get_file(obj):
    try:
        return inspect.getfile(obj)
    except TypeError:
        return None


def _get_source(obj, name=None):
    try:
        src = inspect.getsource(obj)
        if name and not re.search(
            rf"^\s*(def|class)\s+{re.escape(name)}\s*[\(:]", src, re.MULTILINE
        ):
            return None
        return src
    except (OSError, TypeError):
        return None


def _from_history(name):
    """Search xonsh SQLite history for the most recent def or class definition."""
    if XSH.env.get("XONSH_HISTORY_BACKEND", "").lower() != "sqlite":
        return None

    hist = getattr(XSH, "history", None)
    filename = XSH.env.get("XONSH_HISTORY_FILE") or getattr(hist, "filename", None)
    if not filename:
        return None

    start_time = getattr(hist, "start_time", None)
    conn = None
    try:
        conn = sqlite3.connect(str(filename))
        for keyword in ("def", "class"):
            pattern = f"{keyword} {name}%"
            args = (pattern, start_time) if start_time else (pattern,)
            where = "inp LIKE ? AND tsb >= ? ORDER BY tsb DESC LIMIT 20" if start_time else "inp LIKE ? ORDER BY tsb DESC LIMIT 20"
            for (inp,) in conn.execute(f"SELECT inp FROM xonsh_history WHERE {where}", args):
                if re.match(rf"\s*{keyword}\s+{re.escape(name)}\s*[\(:]", inp):
                    return inp.strip()
    except Exception:
        pass
    finally:
        if conn:
            conn.close()
    return None


def _lookup(name):
    """Find name across shell and Python namespaces. Returns (obj, type_str, file_hint)."""
    abbrevs = XSH.ctx.get("abbrevs", {})
    if name in abbrevs:
        return abbrevs[name], "shell-abbreviation", None

    alias = XSH.aliases.get(name)
    if alias is not None:
        if isinstance(alias, list):
            fn = next((f for f in alias if callable(f)), None)
            if fn:
                return getattr(fn, "func", fn), "shell-function", None
            return " ".join(str(t) for t in alias), "shell-alias", None
        elif callable(alias):
            return getattr(alias, "func", alias), "shell-function", None
        return alias, "shell-alias", None

    val = XSH.env.get(name)
    if val is not None:
        return val, "shell-variable", None

    obj = XSH.ctx.get(name)
    if obj is not None:
        return obj, _classify(obj), None

    for mod_name, mod in sys.modules.items():
        if not mod_name.startswith("config"):
            continue
        try:
            obj = getattr(mod, name, None)
        except Exception:
            continue
        if obj is not None and not isinstance(obj, type(sys)):
            return obj, _classify(obj), _get_file(mod)

    path = XSH.commands_cache.locate_binary(name)
    if path and path.startswith("/"):
        return path, "shell-command", None

    return None, None, None


def _classify(obj):
    if inspect.isclass(obj):
        return "class"
    if inspect.ismodule(obj):
        return "module"
    if callable(obj):
        return "function"
    return "variable"


def _build(name, obj, kind, file_hint=None):
    result = {"name": name, "type": kind}
    if kind == "shell-function":
        result["doc"] = inspect.getdoc(obj) or None
        result["file"] = _get_file(obj) or file_hint
        result["source"] = _get_source(obj, name) or _from_history(name)
    elif kind == "shell-alias":
        result["command"] = obj if isinstance(obj, str) else str(obj)
    elif kind == "shell-abbreviation":
        result["expands-to"] = obj if isinstance(obj, str) else "(dynamic)"
    elif kind == "shell-variable":
        result["value"] = str(obj)
    elif kind == "shell-command":
        result["path"] = obj
    elif kind in ("function", "class"):
        result["doc"] = inspect.getdoc(obj) or None
        result["file"] = _get_file(obj) or file_hint
        result["source"] = _get_source(obj, name) or _from_history(name)
    elif kind == "variable":
        result["file"] = file_hint
        result["value"] = repr(obj)
    elif kind == "module":
        result["doc"] = inspect.getdoc(obj) or None
        result["file"] = getattr(obj, "__file__", None)
    return result


def _display(data):
    inline = {k: v for k, v in data.items() if v is not None and not (isinstance(v, str) and "\n" in v)}
    block = {k: v for k, v in data.items() if v is not None and isinstance(v, str) and "\n" in v}

    width = max((len(k) for k in inline), default=0) + 2
    for k, v in inline.items():
        print(f"{(k + ':').ljust(width)} {v}")
    for k, v in block.items():
        print(f"{k}:")
        print(v)


@command
def describe(args):
    """Describe a named command, function, class, variable, or env var.

    Usage: describe [--json] <name>
    """
    if not args:
        print("describe: expected <name>", file=sys.stderr)
        return 1

    as_json = "--json" in args
    names = [a for a in args if a != "--json"]
    if not names:
        print("describe: expected <name>", file=sys.stderr)
        return 1

    name = names[0]
    obj, kind, file_hint = _lookup(name)
    if obj is None:
        print(f"describe: not found: '{name}'", file=sys.stderr)
        return 1

    data = _build(name, obj, kind, file_hint)
    if as_json:
        print(json.dumps(data, indent=2, default=str))
    else:
        _display(data)

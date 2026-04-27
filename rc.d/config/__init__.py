"""
My Xonsh configuration modules.
"""

from importlib import import_module
from xonsh.built_ins import XSH

def command(fn):
    """Register a function as a shell command using its name."""
    XSH.aliases[fn.__name__] = fn
    return fn

def load(*modules):
    """
    Load xonsh config feature modules by name.

    Example:
        config.load("history", "aliases", "zoxide")
    """
    for name in modules:
        import_module(f"{__name__}.{name}")

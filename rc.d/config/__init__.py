"""
My Xonsh configuration modules.
"""

from importlib import import_module

def load(*modules):
    """
    Load xonsh config feature modules by name.

    Example:
        config.load("history", "aliases", "zoxide")
    """
    for name in modules:
        import_module(f"{__name__}.{name}")

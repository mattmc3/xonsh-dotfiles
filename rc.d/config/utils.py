from xonsh.built_ins import XSH

def up_(args):
    """Go up any number of directories"""
    n = int(args[0]) if args else 1
    XSH.execer.exec(f"cd {'../' * n}")
XSH.aliases['up'] = up_

def _juno(args):
    """Jupyter notebook"""
    if not args or len(args) < 1:
        args = ["~/Projects/jupyter"]
    jupyter notebook @(args[0])
aliases['juno'] = _juno

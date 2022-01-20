def shorten_path(path, shortsize=1):
    """Shorten a path string"""
    import re
    # fish does this in prompt_pwd
    path = re.sub(r'^' + $HOME + '($|/)', r'~\1', path)
    return re.sub(r'(\.?[^/]{' + str(shortsize) + r'})[^/]*/', r'\1/', path)

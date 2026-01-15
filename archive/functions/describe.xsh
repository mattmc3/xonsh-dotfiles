def describe(fn):
    """Describe a function"""
    import inspect
    print(inspect.getsource(fn))

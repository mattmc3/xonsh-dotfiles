def _pfd(args):
    """Show the current directory in Finder.app"""
    script = '''tell application "Finder"
                    return POSIX path of (target of first window as text)
                end tell'''
    echo @(script) | osascript err>/dev/null
aliases['pfd']=_pfd

def _pfs(args):
    """Show the current selection in Finder.app"""
    script = '''tell application "Finder" to set the_selection to selection
                if the_selection is not {}
                  repeat with an_item in the_selection
                    log POSIX path of (an_item as text)
                  end repeat
                end if'''
    echo @(script) | osascript err>out
aliases['pfs']=_pfs

from pathlib import Path
import sys

def _pj(args):
    """Project Jump: quickly find a project and cd into it"""
    # make sure we have the fzf utility
    if !(command -v fzf).returncode != 0:
        echo "fzf command not found" out>err
        return 1

    # determine the project home
    if 'PROJECTS' in ${...}:
        prjhome = Path($PROJECTS).resolve()
    else:
        prjhome = Path("~/Projects").resolve()

    if not prjhome.exists():
        print(f"Project home directory not found '{prjhome}'", file=sys.stderr)
        return 1

    # collect all project folders
    projects = [str(f.parent.relative_to($PROJECTS))
                for f in pg`$PROJECTS/**/.git`]
    query = " ".join(args)
    selection = $(echo @("\n".join(projects)) | sort | fzf --layout=reverse-list --query=@(query))
    if selection:
        selection = selection.strip()
        print(f"Taking you to {selection}...")
        dirname = Path($PROJECTS) / selection
        cd @(dirname)
    else:
        return 1

aliases['pj'] = _pj

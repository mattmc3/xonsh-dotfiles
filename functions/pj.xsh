from pathlib import Path

def _get_project_home():
    """Get the home directory for projects"""
    if 'XDG_PROJECTS_DIR' in ${...}:
        return $XDG_PROJECTS_DIR
    else:
        possible_homes = ["projects", "code", "src", "documents", "my documents"]
        possible_homes += [h.title() for h in possible_homes]
        for p in [Path(f"{$HOME}/{d}") for d in possible_homes]:
            if p.exists() and p.is_dir():
                return str(p)

def _pj(args):
    """Project Jump: quickly find a project and cd into it"""
    import inspect
    import re
    from pathlib import Path
    from docopt import docopt, DocoptExit

    usage = (
        inspect.getdoc(_pj),
        "",
        "Usage:",
        "  pj [--stop-dirs=<stop_list>] [<prjhome>]",
        "  pj -h|--help",
        "",
        "Options:",
        "  -h --help                 Show usage",
        "  --stop-dirs=<stop_list>   Stop traversing subdirs if dir found",
        "                            [default: {.bzr,CVS,.git,.hg,.svn,.env,.venv}]",
    )
    try:
        parsed_args = docopt("\n".join(usage), args)
    except DocoptExit:
        echo "Invalid command. Run `pj -h` for proper usage." out>err
        return 1

    # make sure we have the fzf utility
    if !(command -v fzf).returncode != 0:
        echo "fzf command not found" out>err
        return 1

    # determine the project home
    prjhome = parsed_args["<prjhome>"] or _get_project_home()
    prjhome = Path(prjhome)
    if not prjhome.exists():
        echo "Project home directory not found" out>err
        return 1
    else:
        prjhome = prjhome.resolve()

    $PRJ_HOME = @(prjhome)
    projects = [str(f.parent.relative_to(prjhome))
                for f in pg`$PRJ_HOME/**/.git`]
    selection = $(echo @("\n".join(projects)) | fzf)
    if not selection:
        echo "No project was selected"
    else:
        echo "You selected" @(selection)

aliases['pj'] = _pj

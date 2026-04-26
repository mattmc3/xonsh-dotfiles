#!/usr/bin/env python
from xonsh.built_ins import XSH

my_aliases = {
    # 'grep': 'grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn}',
    # one char shortcuts
    'h': 'history show all | less',
    'c': 'clear',
    #  ls shortcuts
    'ls': 'ls -Fh --color=auto',
    'l': 'ls -Fh --color=auto',
    'la': 'ls -lAfh',
    'll': 'ls -lGh',
    'ldot': 'ls -ld .*',
    # misc
    '-': 'cd -',
    'cls': "clear && printf '\\e[3J'",
    'please': 'sudo',
    'zz': 'exit',
    'nv': 'nvim',
    'xsh': 'xonsh',
    # disk usage
    'dud': 'du -d 1 -h',
    'duf': 'du -sh *',
    'dux': 'du -d 1 | sort -n',
    # tar
    'tarls': 'tar -tvf',
    'untar': 'tar -xvf',
    # url
    'urlencode': 'python3 -c "import sys,urllib.parse; print(urllib.parse.quote(sys.stdin.read().strip()))"',
    'urldecode': 'python3 -c "import sys,urllib.parse; print(urllib.parse.unquote(sys.stdin.read().strip()))"',
    # date/time
    'timestamp': "date '+%Y-%m-%d %H:%M:%S'",
    'datestamp': "date '+%Y-%m-%d'",
    'isodate': "date +%Y-%m-%dT%H:%M:%S%z",
    'utc': "date -u +%Y-%m-%dT%H:%M:%SZ",
    'unixepoch': "date +%s",
    # quick dirs
    'dotf': 'cd $DOTFILES',
    'dotfl': 'cd $DOTFILES.local',
    'fishconf': 'cd ~/.config/fish',
    'fdot': 'cd ~/.config/fish',
    'xdot': 'cd ~/.config/xonsh',
    'zdot': 'cd ~/.config/zsh',
}
XSH.aliases.update(my_aliases)

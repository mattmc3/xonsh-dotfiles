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
    # macos
    'brewup': 'brew update && brew upgrade && brew cleanup',
    # misc
    'zz': 'exit',
    'nv': 'nvim',
    'xsh': 'xonsh',
    # quick dirs
    'dotf': 'cd $DOTFILES',
    'dotfl': 'cd $DOTFILES.local',
    'fishconf': 'cd ~/.config/fish',
    'fdot': 'cd ~/.config/fish',
    'xdot': 'cd ~/.config/xonsh',
    'zdot': 'cd ~/.config/zsh',
}
XSH.aliases.update(my_aliases)

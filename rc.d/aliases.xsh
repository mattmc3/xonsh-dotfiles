# aliases
myaliases = {
    # 'grep': 'grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn}',
    # one char shortcuts
    'h': 'history show all | less',
    'c': 'clear',
    #  ls shortcuts
    'ls': 'ls -GF',
    'l': 'ls -F',
    'la': 'ls -lAfh',
    'll': 'ls -lFh',
    'ldot': 'ls -ld .*',
    # macos
    'brewup': 'brew update && brew upgrade',
    'xshrc': 'nvim ~/.config/xonsh/xsh.rc',
    # misc
    'zz': 'exit',
    'nv': 'nvim',
    'xsh': 'xonsh',
    # quick dirs
    'prj': 'cd ~/Projects',
    'dotf': 'cd $DOTFILES',
    'dotfl': 'cd $DOTFILES.local',
    'fishconf': 'cd ~/.config/fish',
    'xdot': 'cd ~/.config/xonsh',
    'zdot': 'cd ~/.config/zsh',
}
aliases.update(myaliases)

# set the path
user_bins = [
    # user bins
    p'~/bin',

    # override bins
    p'/opt/homebrew/bin',
    p'/opt/homebrew/sbin',
    p'/usr/local/bin',
    p'/usr/local/sbin',

    # system bins
    p'/usr/bin',
    p'/bin',
    p'/usr/sbin',
    p'/sbin',

    # golang bins
    p'/usr/local/opt/go/libexec/bin',
    p'~/Projects/golang/bin',

    # emacs bins
    p'~/.emacs.d/bin',
    p'~/.config/emacs/bin',

    # node.js bins
    p'/usr/local/share/npm/bin',

    # ruby bins
    p'/usr/local/opt/ruby/bin',
]
$PATH.clear()
for bindir in user_bins:
    if bindir.exists():
        $PATH.add(bindir, replace=True)

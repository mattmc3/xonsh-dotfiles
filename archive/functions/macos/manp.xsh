def _manp(args):
    if not args or len(args) < 1:
        echo "What manual page do you want?" out>err
        return 1
    for page in args:
        man -t @(page) | open -f -a Preview
aliases['manp']=_manp

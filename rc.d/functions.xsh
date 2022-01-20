# use a functions dir for all the xonsh goodies
$XONSH_FUNC_DIR=p"$XONSH_CONFIG_DIR/functions"
for f in pg`$XONSH_FUNC_DIR/**/*`:
    if not f.is_dir():
        source @(f)

# https://github.com/starship/starship/discussions/1908
$STARSHIP_CONFIG = p"~/.config/xonsh/misc/starship.toml"
execx($(starship init xonsh))

# native prompt
# customize the prompt: https://xon.sh/tutorial.html#customizing-the-prompt
# Change git vars
# $XONSH_GITSTATUS_LINES_ADDED=''
# $XONSH_GITSTATUS_LINES_REMOVED=''
# $XONSH_GITSTATUS_CHANGED=''
# $XONSH_GITSTATUS_DELETED=''
# $XONSH_GITSTATUS_UNTRACKED=''
# # set prompt
# $PROMPT = '{CYAN}{short_cwd} {INTENSE_GREEN}❯{RESET} '
# $RIGHT_PROMPT = '{BOLD_GREEN}{gitstatus}{RESET}'

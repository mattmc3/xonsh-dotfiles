#!/usr/bin/env python
import argparse
import os
import subprocess
import sys
from pathlib import Path

from config import command


def _git_config(key, default=None):
    result = subprocess.run(
        ['git', 'config', '--global', key],
        capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else default


def _cloner_config(profile=None):
    """Read cloner config, with profile-specific keys overriding defaults."""
    def get(key, default=None):
        if profile:
            val = _git_config(f'cloner.{profile}.{key}')
            if val is not None:
                return val
        return _git_config(f'cloner.{key}', default)

    raw_flags = get('cloneaddflags', '')
    ssh_key_str = get('sshkey', '')
    return {
        'repo_path': Path(get('repopath', '~/Projects')).expanduser(),
        'owner':     get('gitowner', ''),
        'domain':    get('gitdomain', 'github.com'),
        'protocol':  get('gitprotocol', 'https'),
        'flags':     raw_flags.split() if raw_flags else [],
        'ssh_key':   Path(ssh_key_str).expanduser() if ssh_key_str else None,
    }


def _clone_url(protocol, domain, owner, repo):
    if protocol == 'git':
        return f'git@{domain}:{owner}/{repo}'
    elif protocol == 'ssh':
        return f'ssh://git@{domain}/{owner}/{repo}'
    else:
        return f'https://{domain}/{owner}/{repo}'


@command
def cloner(args):
    """Clone a git repo using [cloner] config from ~/.config/git/config.

    Usage:
      cloner [--profile=<name>] <repo>              # default owner and path
      cloner [--profile=<name>] <owner>/<repo>      # explicit owner
      cloner [--profile=<name>] <repo> <dest-base>  # explicit base path

    Profiles map to [cloner "<name>"] subsections in git config, falling
    back to [cloner] defaults for any unset keys.
    """
    p = argparse.ArgumentParser(prog='cloner', exit_on_error=False)
    p.add_argument('--profile', '-p', default=None, metavar='NAME')
    p.add_argument('repo')
    p.add_argument('dest_base', nargs='?')

    try:
        ns, extra_flags = p.parse_known_args(args)
    except (argparse.ArgumentError, SystemExit):
        p.print_usage(sys.stderr)
        return 1

    cfg = _cloner_config(ns.profile)

    if '/' in ns.repo:
        owner, repo = ns.repo.split('/', 1)
    else:
        owner, repo = cfg['owner'], ns.repo

    dest_base = Path(ns.dest_base).expanduser() if ns.dest_base else cfg['repo_path']
    dest = dest_base / owner / repo

    if dest.exists():
        print(f"cloner: already exists — changing to {dest}", file=sys.stderr)
        os.chdir(dest)
        return

    url = _clone_url(cfg['protocol'], cfg['domain'], owner, repo)
    dest.parent.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    if cfg['ssh_key'] and cfg['protocol'] == 'git':
        env['GIT_SSH_COMMAND'] = f'ssh -F /dev/null -i {cfg["ssh_key"]} -o IdentitiesOnly=yes'

    result = subprocess.run(
        ['git', 'clone'] + cfg['flags'] + extra_flags + [url, str(dest)],
        env=env,
    )

    if result.returncode == 0:
        os.chdir(dest)
    else:
        return result.returncode

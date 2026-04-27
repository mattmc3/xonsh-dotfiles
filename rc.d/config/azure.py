#!/usr/bin/env python
import shutil
import subprocess
import sys

from config import command
from xonsh.built_ins import XSH

if shutil.which('az'):
    @command
    def azdbtok(args):
        """Get an Azure Database access token and copy it to clipboard."""
        result = subprocess.run([
            'az', 'account', 'get-access-token',
            '--resource', 'https://ossrdbms-aad.database.windows.net',
            '--query', 'accessToken',
            '--output', 'tsv',
        ], capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stderr.strip(), file=sys.stderr)
            return result.returncode
        token = result.stdout.strip()
        print(token)
        import pyperclip
        pyperclip.copy(token)

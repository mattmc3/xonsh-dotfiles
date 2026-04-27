#!/usr/bin/env python
import os
import signal
from prompt_toolkit.document import Document
from xonsh.built_ins import XSH
from xonsh.events import events


@events.on_ptk_create
def _setup_symmetric_ctrl_z(bindings, **kwargs):
    @bindings.add("c-z")
    def symmetric_ctrl_z(event):
        buf = event.app.current_buffer
        if not buf.text and XSH.all_jobs:
            buf.set_document(Document("fg"))
            buf.validate_and_handle()
        else:
            os.kill(os.getpid(), signal.SIGTSTP)

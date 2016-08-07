# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import signal
import logging


def register_signal_listener(signaller, listener):
    def on_signal(signum=None, frame=None):
        logging.info('SIGNAL %d received', signum or 0)
        listener(signum)

    for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGABRT, signal.SIGQUIT,
                signal.SIGALRM, signal.SIGHUP, signal.SIGUSR1, signal.SIGUSR2]:
        signaller.signal(sig, on_signal)

import signal
import logging


def is_exit_signal(signum):
    return signum in [signal.SIGTERM, signal.SIGINT,
                      signal.SIGABRT, signal.SIGQUIT]


def register_signal_listener(listener):
    def on_signal(signum=None, frame=None):
        logging.info('SIGNAL %d received', signum)
        listener(signum)

    for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGABRT, signal.SIGQUIT,
                signal.SIGALRM, signal.SIGHUP, signal.SIGUSR1, signal.SIGUSR2]:
        signal.signal(sig, on_signal)

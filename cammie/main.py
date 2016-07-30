#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import argparse
import logging.config

import gevent
from gevent.wsgi import WSGIServer

from cammie.runtime import register_signal_listener, is_exit_signal


def main():
    parser = argparse.ArgumentParser(
        description='Run the Cammie baby monitor server')
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='enables debug run of server')
    parser.add_argument(
        '-l', '--log-level', default='INFO',
        help='logging level for the server'
    )

    args = parser.parse_args()

    log_config = {
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG'
            }
        },
        'root': {
            'level': getattr(logging, args.log_level)
        }
    }
    logging.config.dictConfig(log_config)

    # start A/V on separate threads. incoming requests view stream based on
    # injected A/V state
    from cammie.record import VideoCamera, AudioRecorder
    camera = VideoCamera()
    camera.start()
    audio = AudioRecorder()
    audio.start()

    from cammie.website import app
    app.camera = camera
    app.audio = audio
    app.debug = args.debug or False

    http_server = WSGIServer(('0.0.0.0', 5000), app)

    # handle shutdown signals gracefully
    def shutdown(signum):
        audio.destroy()
        camera.destroy()
        http_server.stop()
    register_signal_listener(gevent, shutdown)

    http_server.serve_forever()


if __name__ == '__main__':
    main()

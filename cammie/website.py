#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from flask import Flask, render_template, Response

app = Flask(__name__)
boundary = b'593247982374923'


@app.route('/')
def index():
    return render_template('index.html')


def frame_generator(cur_camera):
    while True:
        frame = cur_camera.current_frame or ''
        yield (b'--' + boundary + b'\r\n' +
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(
        frame_generator(app.camera),
        mimetype='multipart/x-mixed-replace; boundary={}'.format(boundary)
    )

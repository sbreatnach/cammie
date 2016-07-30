# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from flask import Flask, render_template, Response

app = Flask(__name__)
boundary = b'593247982374923'


@app.route('/')
def index():
    return render_template('index.html')


def frame_generator(cur_input, content_type):
    while True:
        next_data = cur_input.current_data or ''
        yield (b'--{}\r\n'
               b'Content-Type: {}\r\n\r\n'
               b'{}\r\n\r\n'.format(boundary, content_type, next_data))


def generator(cur_input):
    while True:
        yield cur_input.current_data or b''


@app.route('/video_feed')
def video_feed():
    return Response(
        frame_generator(app.camera, b'image/jpeg'),
        mimetype='multipart/x-mixed-replace; boundary={}'.format(boundary)
    )


@app.route('/audio_feed')
def audio_feed():
    return Response(
        generator(app.audio), mimetype='audio/x-wav'
    )

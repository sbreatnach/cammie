# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from flask import Flask, render_template, Response

app = Flask(__name__)


def create_mixed_generator(content_type):
    boundary = b'593247982374923'

    def frame_generator(recorder):
        while True:
            next_data = recorder.current_data or ''
            yield (b'--{}\r\n'
                   b'Content-Type: {}\r\n\r\n'
                   b'{}\r\n\r\n'.format(boundary,
                                        content_type.encode('ascii'),
                                        next_data))

    mime_type = 'multipart/x-mixed-replace; boundary={}'.format(boundary)
    return frame_generator, mime_type


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    frame_generator, mime_type = create_mixed_generator('image/jpeg')
    return Response(frame_generator(app.camera), mimetype=mime_type)

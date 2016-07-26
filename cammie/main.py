#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import time
from flask import Flask, render_template, Response

from cammie.camera import VideoCamera

app = Flask(__name__)
is_running = True


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while is_running:
        success, frame = camera.get_frame()
        while not success:
            time.sleep(0.1)
            success, frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def main():
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()

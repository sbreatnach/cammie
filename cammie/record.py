# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from threading import Thread
import time

import pyaudio
import cv2


class VideoCamera(Thread):
    def __init__(self, *args, **kwargs):
        super(VideoCamera, self).__init__(*args, **kwargs)
        self._video = None
        self.current_data = None
        self.is_running = False

    def __del__(self):
        self.destroy()

    @property
    def video(self):
        if self._video is None:
            # device ID varies based on hardware combinations
            self._video = cv2.VideoCapture()
            device_id = -1
            while not self._video.isOpened() and device_id < 10:
                self._video.open(device_id)
            if device_id == 10:
                # FIXME: log and fail completely
                print 'Failed to initialise video device'
        return self._video

    def destroy(self):
        self.is_running = False
        if self._video is not None:
            try:
                self._video.release()
            except:
                pass
            self._video = None

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, output = False, ''
        if success:
            ret, jpeg = cv2.imencode('.jpg', image)
            output = jpeg.tostring()
        return success and ret, output

    def run(self):
        self.is_running = True
        while self.is_running:
            success, frame = self.get_frame()
            if success:
                self.current_data = frame
            # attempt 12fps
            time.sleep(1.0/12.0)


class AudioRecorder(Thread):

    def __init__(self, *args, **kwargs):
        super(AudioRecorder, self).__init__(*args, **kwargs)
        self.audio = pyaudio.PyAudio()
        self._stream = None
        self.buffer_size = 1024
        self.current_data = None
        self.is_running = False

    @property
    def stream(self):
        if self._stream is None:
            self._stream = self.audio.open(format=pyaudio.paInt16,
                                           channels=2,
                                           rate=44100,
                                           input=True,
                                           frames_per_buffer=self.buffer_size)
        return self._stream

    def destroy(self):
        self.is_running = False
        if self._stream is not None:
            try:
                self._stream.stop_stream()
            except:
                pass
            finally:
                self._stream.close()
            self._stream = None

    def run(self):
        self.stream.start_stream()
        self.is_running = True
        while self.is_running:
            self.current_data = self.stream.read(self.buffer_size)

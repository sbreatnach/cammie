# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from threading import Thread, Lock
import time

import cv2


class VideoCamera(Thread):
    def __init__(self, *args, **kwargs):
        super(VideoCamera, self).__init__(*args, **kwargs)
        self._video = None
        self.current_data = None
        self.is_running = False
        self._lock = Lock()

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
        with self._lock:
            if self._video is not None:
                try:
                    self._video.release()
                except:
                    pass
                self._video = None

    def get_frame(self):
        with self._lock:
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
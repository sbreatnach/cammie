from gevent.wsgi import WSGIServer

from cammie.website import app
from cammie.video import VideoCamera


def main():
    # start camera on separate thread. incoming requests view images based on
    # injected camera state
    camera = VideoCamera()
    camera.start()
    app.camera = camera

    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()


if __name__ == '__main__':
    main()

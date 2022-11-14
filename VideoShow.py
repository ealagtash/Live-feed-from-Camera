from threading import Thread
import cv2

class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            ret, buffer = cv2.imencode('.jpeg',self.frame)
            self.frame = buffer.tobytes()
            yield self.frame

    def stop(self):
        self.stopped = True
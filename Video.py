import cv2
import imutils
import time
import argparse
import imutils
import time
from threading import Thread
from VideoGet import VideoGet
from VideoShow import VideoShow
from flask import Flask, render_template, Response, stream_with_context, request

app = Flask('__name__')

def video_stream():
    pTime=0
    
    video_getter = VideoGet(0).start()
    video_shower = VideoShow(video_getter.frame).start()
    
    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        video_shower.frame = video_getter.frame
        frame = video_getter.frame
        imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        cTime=time.time()
        fps= 1/(cTime - pTime)
        pTime =cTime
        cv2.putText(frame, f'FPS:{int(fps)}',(20,70),cv2.FONT_HERSHEY_PLAIN,3,(255, 255, 0), 2)
        frame = next(video_shower.show())
        yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame +b'\r\n')
    


@app.route('/camera')
def camera():
    return render_template('camera.html')


@app.route('/video_feed')
def video_feed():
    tmp =Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return tmp


app.run(host='0.0.0.0', port='8080', debug=False)

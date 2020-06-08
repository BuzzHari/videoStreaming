from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.gzip import gzip_page
import cv2 as cv
import numpy as np
import threading

class VideoCamera(object):
  def __init__(self):
    # Caputuring video from webcam using OpenCV.
    # A video file can also be used instead.
    self.video = cv.VideoCapture(0)

  def __del__(self):
    self.video.release()

  def get_frame(self):
    success, image = self.video.read()
    # Enconding raw image to jpg.
    ret, jpeg = cv.imencode('.jpg', image)
    return jpeg.tobytes()
  
  def update(self):
    while True:
      (self.grabbed, self.frame) = self.video.read()


def gen(camera):
  while True:
    frame = camera.get_frame()
    yield(b'--frame\r\n'
          b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def index(request):
  return render(request, 'camera_app/index.html')

@gzip_page
def livefeed(request):
  try:
    # Sending as an multipart response.
    # Where each part has a frame of jpeg type.
    return StreamingHttpResponse(gen(VideoCamera()), 
              content_type="multipart/x-mixed-replace;boundary=frame")
  except:
    pass
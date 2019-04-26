import picamera
import os
camera = picamera.PiCamera()

camera.start_preview()
camera.capture('setup.png')
camera.stop_preview()


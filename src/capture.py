import picamera
import os
camera = picamera.PiCamera()
moveDir = os.path.dirname(os.path.realpath(__file__)) + '/../phys/'

def capture():
    global camera
    global moveDir
    camera.start_preview()
    camera.capture(moveDir + 'previous.png')
    camera.stop_preview()

def capture2():
    global camera
    global moveDir
    camera.start_preview()
    camera.capture(moveDir + 'current.png')
    camera.stop_preview()

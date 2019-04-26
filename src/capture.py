import picamera
import os
#camera = picamera.PiCamera()
moveDir = os.path.dirname(os.path.realpath(__file__)) + '/../phys/'

def capture():
    
    global moveDir

    """
    global camera
    camera.start_preview()
    camera.capture(moveDir + 'previous.png')
    camera.stop_preview()
    """
    os.system("raspistill -o \"" + moveDir + "previous.png\"")

def capture2():
    global moveDir
    """
    global camera
    camera.start_preview()
    camera.capture(moveDir + 'current.png')
    camera.stop_preview()
    """
    os.system("raspistill -o \"" + moveDir + "current.png\"")

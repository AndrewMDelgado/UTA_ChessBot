import picamera
from os.path import dirname, realpath
from os import system
#camera = picamera.PiCamera()


def capture(filename):
    moveDir = dirname(realpath(__file__)) + '/../phys/'
    system("raspistill -o \"" + moveDir + filename + "\"")

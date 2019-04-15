import picamera

def capture():
    
    camera = picamera.PiCamera()
    camera.start_preview()
    camera.capture('previous.png')
    camera.stop_preview()

def capture2():
    camera = picamera.PiCamera()
    camera.start_preview()
    camera.capture('current.png')
    camera.stop_preview()

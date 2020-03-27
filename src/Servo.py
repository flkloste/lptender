class Servo(object):
    def __init__(self, gpioController, gpioCtrlPin):
        self._gpioController = gpioController
        self._gpioCtrlPin = gpioCtrlPin

    def setAngle(self, angle):
        raise RuntimeError("Not implemented!")
        
    def dontMove(self):
        self._gpioController.setServoPulseWidth(self._gpioCtrlPin, 0)

class ServoDS3218_270(Servo):
    def __init__(self, gpioController, gpioCtrlPin):
        super(ServoDS3218_270, self).__init__(gpioController, gpioCtrlPin)
    
    def setAngle(self, angle):
        if not (0 <= angle <= 270): 
            raise RuntimeError("Angle out of range. (angle=%s)" % str(angle))

        pulseWidth = int(500 + 2000.0 / 270.0 * angle)
        self._gpioController.setServoPulseWidth(self._gpioCtrlPin, pulseWidth)
        
class ServoDS3218_180(Servo):
    def __init__(self, gpioController, gpioCtrlPin):
        super(ServoDS3218_180, self).__init__(gpioController, gpioCtrlPin)
    
    def setAngle(self, angle):
        if not (0 <= angle <= 180): 
            raise RuntimeError("Angle out of range. (angle=%s)" % str(angle))
 
        pulseWidth = int(500 + 2000.0 / 180.0 * angle)
        self._gpioController.setServoPulseWidth(self._gpioCtrlPin, pulseWidth)

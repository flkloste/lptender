class Servo:
    
    def __init__(self, globalGPIO, gpioControl):
        self._gpio = globalGPIO
        self._gpioControl = gpioControl
        self._frequency = 50
        
        # setup control GPIO for PWM
        self._gpio.setupOutput(self._gpioControl)
        self._pwm = self._gpio.pwm(self._gpioControl, self._frequency)
        self._pwm.start(0)
        
    def setAngle(self, angle):
        raise RuntimeError("Not implemented!")
        
    def dontMove(self):
        self._pwm.ChangeDutyCycle(0)

class ServoDS3218_270(Servo):
    def __init__(self, globalGPIO, gpioControl):
        super(ServoDS3218_270, self).__init__(globalGPIO, gpioControl)
    
    def setAngle(self, angle):
        if not (0 <= angle <= 270): 
            raise RuntimeError("Angle out of range. (angle=%s)" % str(angle))
 
        dutyCycle = 2.22222222 + 10.0 / 270.0 * angle
        self._pwm.ChangeDutyCycle(dutyCycle)
        
class ServoDS3218_180(Servo):
    def __init__(self, globalGPIO, gpioControl):
        super(ServoDS3218_180, self).__init__(globalGPIO, gpioControl)
    
    def setAngle(self, angle):
       # if not (0 <= angle <= 180): 
        #    raise RuntimeError("Angle out of range. (angle=%s)" % str(angle))
 
       # dutyCycle = 2.22222222 + 10.0 / 270.0 * angle
        print dutyCycle
        self._pwm.ChangeDutyCycle(dutyCycle)
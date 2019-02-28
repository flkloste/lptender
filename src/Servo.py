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
        if not (0 <= angle <= 270): 
            raise RuntimeError("Angle out of range. (angle=%s)" % str(angle))
 
        dutyCycle = 2.22222222 + 10.0 / 270.0 * angle
        print dutyCycle
        self._pwm.ChangeDutyCycle(dutyCycle)
        
    def dontMove(self):
        self._pwm.ChangeDutyCycle(0)

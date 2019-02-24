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
        dutyCycle = ((angle/180.0) + 1.0) * 5.0
        self._pwm.ChangeDutyCycle(dutyCycle)
        
    def dontMove(self):
        self._pwm.ChangeDutyCycle(0)
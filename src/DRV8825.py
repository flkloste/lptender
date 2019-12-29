from time import sleep
from math import exp
import StepperUtils

def noPwm(func):
    def deco(self, *args, **kwargs):
        if self._pwmActive == True:
            self._gpio.stopPwm(self._gpioStep)
            self._pwmActive = False
        func(self, *args, **kwargs)
    return deco


class DRV8825:

    def __init__(self, globalGPIO, gpioStep, gpioDirection):
        self._gpio = globalGPIO
        self._gpioStep = gpioStep
        self._gpioDirection = gpioDirection
        
        self.PWM_FREQUENCY_FAST = 4000
        self.PWM_FREQUENCY_SLOW = 250

        # setup step GPIO
        self._gpio.setupOutput(self._gpioStep)
        self._gpio.output(self._gpioStep, self._gpio.levelLow())
        
        # setup direction GPIO
        self._gpio.setupOutput(self._gpioDirection)
        self._gpio.output(self._gpioDirection, self.clockWise())

        self._pwmActive = False
    
    @noPwm
    def move(self, steps, direction):
        if steps not in range(100001):
            raise RuntimeError("Steps out of range. (steps=%s)" % str(steps))
        
        if direction not in [self.clockWise(), self.counterClockWise()]:
            raise RuntimeError("Direction has an invalid value: %s" % str(direction))
    
        self._gpio.output(self._gpioDirection, direction)
    
        ramp = StepperUtils.calcRamp(steps)
        waitSecs = StepperUtils.calcSecsUntilRampFinished(ramp)
        self._gpio.generate_ramp(ramp, self._gpioStep)
        sleep(waitSecs)
        
    def moveUntilStopped(self, direction, speed):
        if speed not in [self.PWM_FREQUENCY_SLOW, self.PWM_FREQUENCY_FAST]:
            raise RuntimeError("Speed has an invalid value: %s" % str(speed))

        if direction not in [self.clockWise(), self.counterClockWise()]:
            raise RuntimeError("Direction has an invalid value: %s" % str(direction))
            
        self._gpio.output(self._gpioDirection, direction)
        self._gpio.setPwm(self._gpioStep, 128, speed)
        self._pwmActive = True 

    @noPwm
    def stop(self):
        pass
    
    def clockWise(self):
        return self._gpio.levelLow()
        
    def counterClockWise(self):
        return self._gpio.levelHigh()



from time import sleep
from math import exp

class DRV8825:

    def __init__(self, globalGPIO, gpioStep, gpioDirection):
        self._gpio = globalGPIO
        self._gpioStep = gpioStep
        self._gpioDirection = gpioDirection
        self.MIN_DELAY = 0.0001
        self.MAX_DELAY = 0.02
                
        # setup step GPIO
        self._gpio.setupOutput(self._gpioStep)
        self._gpio.output(self._gpioStep, self._gpio.levelLow())
        
        # setup direction GPIO
        self._gpio.setupOutput(self._gpioDirection)
        self._gpio.output(self._gpioDirection, self.clockWise())
    
    def move(self, steps, direction):
        if steps not in range(100000):
            raise RuntimeError("Steps out of range. (steps=%s)" % str(steps))
        
        if direction not in [self.clockWise(), self.counterClockWise()]:
            raise RuntimeError("Direction has an invalid value: %s" % str(direction))
    
        self._gpio.output(self._gpioDirection, direction)
    
        for step in range(steps):
            delay = self.MIN_DELAY
            self._gpio.output(self._gpioStep, self._gpio.levelHigh())
            sleep(delay)
            self._gpio.output(self._gpioStep, self._gpio.levelLow())
            sleep(delay)
            
    def moveSingleStepSlow(self, direction):
        if direction not in [self.clockWise(), self.counterClockWise()]:
            raise RuntimeError("Direction has an invalid value: %s" % str(direction))
            
        self._gpio.output(self._gpioDirection, direction)
        self._gpio.output(self._gpioStep, self._gpio.levelHigh())
        sleep(self.MAX_DELAY)
        self._gpio.output(self._gpioStep, self._gpio.levelLow())
        sleep(self.MAX_DELAY)
        
    def moveSingleStepFast(self, direction):
        if direction not in [self.clockWise(), self.counterClockWise()]:
            raise RuntimeError("Direction has an invalid value: %s" % str(direction))
            
        self._gpio.output(self._gpioDirection, direction)
        self._gpio.output(self._gpioStep, self._gpio.levelHigh())
        sleep(self.MIN_DELAY)
        self._gpio.output(self._gpioStep, self._gpio.levelLow())
        sleep(self.MIN_DELAY)
    
    def clockWise(self):
        return self._gpio.levelHigh()
        
    def counterClockWise(self):
        return self._gpio.levelLow()



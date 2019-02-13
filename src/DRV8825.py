from time import sleep

class DRV8825:

    def __init__(self, globalGPIO, gpioStep, gpioDirection):
        self._gpio = globalGPIO
        self._gpioStep = gpioStep
        self._gpioDirection = gpioDirection
        self.MIN_DELAY = 0.0004
        self.MAX_DELAY = 0.02
                
        # setup step GPIO
        self._gpio.setupOutput(self._gpioStep)
        self._gpio.output(self._gpioStep, self._gpio.levelLow())
        
        # setup direction GPIO
        self._gpio.setupOutput(self._gpioDirection)
        self._gpio.output(self._gpioDirection, self.clockWise())
    
    # create a smooth ramping by applying an inverse sigmoid function to the delay values
    def CalcDelayRamp(self, step):
        return self.MIN_DELAY + 1/(1+math.exp(float(step)/20-5)) * self.MAX_DELAY
    
    def move(self, steps, direction):
        if steps < 0:
            raise RuntimeError("Steps must not be negative. (steps=%s)" % str(steps))
        
        if direction not in [self.clockWise(), self.counterClockWise()]:
            raise RuntimeError("Direction has an invalid value: %s" % str(direction))
    
        self._gpio.output(self._gpioDirection, direction)
    
        for step in range(steps):
            delay = self.CalcDelayRamp(step)
            self._gpio.output(self._gpioStep, self._gpio.levelHigh())
            sleep(delay)
            self._gpio.output(self._gpioStep, self._gpio.levelLow())
            sleep(delay)
    
    def clockWise(self):
        return self._gpio.levelHigh()
        
    def counterClockWise(self):
        return self._gpio.levelLow()



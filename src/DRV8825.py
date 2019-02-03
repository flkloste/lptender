from time import sleep

class DRV8825:

    def __init__(self, globalGPIO, gpioStep, gpioDirection):
        self._gpio = globalGPIO
        self._gpioStep = gpioStep
        self._gpioDirection = gpioDirection
        self._delay = 0.0004
        
        self.currentDirection = self.clockWise()
                
        # setup step GPIO
        self._gpio.setup(self._gpioStep, self._gpio.modeOutput())
        self._gpio.setup(self._gpioStep, self._gpio.levelLow())
        
        # setup direction GPIO
        self._gpio.setup(self._gpioDirection, self._gpio.modeOutput())
        self._gpio.output(self._gpioDirection, self.clockWise())
        
    def getDirection(self):
        return self.currentDirection
        
    def setDirection(self, direction):
        if direction not in [self.clockWise(), self.counterClockWise()]:
            raise RuntimeError("Direction has an invalid value")
    
        self._gpio.output(self._gpioDirection, direction)
        self.currentDirection = direction
        
    def move(self, steps):
        self.move(steps, self.currentDirection)
        
    def move(self, steps, direction):
        if steps < 0:
            raise RuntimeError("Steps must not be negative. (steps=%d)" % steps)
    
        self.setDirection(direction)
    
        for i in range(steps):
            self._gpio.output(self._gpioStep, self._gpio.levelHigh())
            sleep(self._delay)
            self._gpio.output(self._gpioStep, self._gpio.levelLow())
            sleep(self._delay)
    
    def clockWise():
        return 1
        
    def counterClockWise():
        return 0



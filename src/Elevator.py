import DRV8825

class Elevator:
    
    def __init__(self, globalGPIO):
        self._gpioStep = 21
        self._gpioDirection = 20
        self._drv8825 = DRV8825(globalGPIO, self._gpioStep, self._gpioDirection)
    
    def moveUp(steps):
        self._drv8825.move(steps, self._drv8825.clockWise())
    
    def moveDown(steps):
        self._drv8825.move(steps, self._drv8825.counterClockWise())


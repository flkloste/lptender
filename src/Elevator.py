import DRV8825
import Endstop
from time import sleep

class Elevator:
    
    def __init__(self, globalGPIO):
        self._gpioStep = 21
        self._gpioDirection = 20
        self._gpioEndstopSignal = 4
        self._drv8825 = DRV8825.DRV8825(globalGPIO, self._gpioStep, self._gpioDirection)
        self._endstop = Endstop.Endstop(globalGPIO, self._gpioEndstopSignal)
    
    def moveUp(self, steps):
        self._drv8825.move(steps, self._drv8825.clockWise())
    
    def moveDown(self, steps):
        self._drv8825.move(steps, self._drv8825.counterClockWise())

    def gotoHome(self, steps):
        # move down until endstop is reached
        while not _endstop.isClosed():
            self.moveDown(1)
            sleep(0.004)
            
        # endstop is reached
        while _endstop.isClosed():
            self.moveUp(1)
            sleep(0.01)
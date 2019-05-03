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
        sleep(1)
    
    def moveDown(self, steps):
        self._drv8825.move(steps, self._drv8825.counterClockWise())
        sleep(1)

    def gotoHome(self):
        # move up until endstop is reached
        while not self._endstop.isClosed():
            self._drv8825.moveSingleStepFast(self._drv8825.clockWise())
            
        # endstop is reached
        while self._endstop.isClosed():
            self._drv8825.moveSingleStepSlow(self._drv8825.counterClockWise())

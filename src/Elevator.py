import DRV8825
from time import sleep

class Elevator:
    
    class Endstop:        
        def __init__(self, globalGPIO, gpioSignal):
            self._gpio = globalGPIO
            self._gpioSignal = gpioSignal
            
            # setup signal GPIO
            self._gpio.setupInput(self._gpioSignal, self._gpio.inputPullDown())
            
        def isClosed(self):
            return bool(self._gpio.input(self._gpioSignal))

    def __init__(self, config, globalGPIO):
        self._gpioStep =  config.elevator.gpioStep #21
        self._gpioDirection = config.elevator.gpioDirection #20
        self._gpioEndstopSignal = config.elevator.gpioEndstopSignal #4
        self._drv8825 = DRV8825.DRV8825(globalGPIO, self._gpioStep, self._gpioDirection)
        self._endstop = Elevator.Endstop(globalGPIO, self._gpioEndstopSignal)
    
    def moveUp(self, steps):
        self._drv8825.move(steps, self._drv8825.clockWise())
        sleep(1)
    
    def moveDown(self, steps):
        self._drv8825.move(steps, self._drv8825.counterClockWise())
        sleep(1)

    def gotoHome(self):
        # move up until endstop is reached
        if not self._endstop.isClosed():
            self._drv8825.moveUntilStopped(self._drv8825.clockWise(), self._drv8825.PWM_FREQUENCY_FAST)

        while not self._endstop.isClosed():
            sleep(0.01)

        self._drv8825.stop()
            
        # endstop is reached
        if self._endstop.isClosed():
            self._drv8825.moveUntilStopped(self._drv8825.counterClockWise(), self._drv8825.PWM_FREQUENCY_SLOW)

        while not self._endstop.isClosed():
            sleep(0.01)
        
        self._drv8825.stop()

        sleep(1)

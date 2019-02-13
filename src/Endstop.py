class Endstop:
    
    def __init__(self, globalGPIO, gpioSignal):
        self._gpio = globalGPIO
        self._gpioSignal = gpioSignal
        
        # setup signal GPIO
        self._gpio.setupInput(self._gpioSignal, self._gpio.inputPullDown())
        
    def isClosed(self):
        return self._gpio.input(self._gpioSignal)
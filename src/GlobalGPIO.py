import RPi.GPIO as GPIO

class GlobalGPIO:
    
    def __init__(self):
        self.usedGPIOs = list()    
        GPIO.setmode(GPIO.BCM)
        
    def __del__(self):
        GPIO.cleanup()

    def setup(self, gpioBcmNo, mode):
        if gpioBcmNo in self.usedGPIOs:
            raise RuntimeError("GPIO %s already in use!" % str(gpioBcmNo))
        GPIO.setup(gpioBcmNo, mode)
    
    def output(self, gpioBcmNo,level):
        if gpioBcmNo not in self.usedGPIOs:
            raise RuntimeError("GPI %s has not been set up!" % str(gpioBcmNo))
        GPIO.output(gpioBcmNo, level)
    
    def modeInput(self):
        return GPIO.IN
        
    def modeOutput(self):
        return GPIO.OUT

    def levelHigh(self):
        return GPIO.HIGH

    def levelLow(self):
        return GPIO.LOW



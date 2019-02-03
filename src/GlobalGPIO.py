import RPi.GPIO as GPIO

class GlobalGPIO:
    
    def __init__(self):
        self.usedGPIOs = list()    
        GPIO.setmode(GPIO.BCM)
        
    def __del__(self):
        GPIO.cleanup()

    def setup(self, gpioBcmNo, mode):
        if mode not in [self.modeInput(), self.modeOutput()]:
            raise RuntimeError("Paramter 'mode' has an invalid value: %s" % str(mode))
            
        if gpioBcmNo in self.usedGPIOs:
            raise RuntimeError("GPIO %s already in use!" % str(gpioBcmNo))
            
        GPIO.setup(gpioBcmNo, mode)
        self.usedGPIOs.append(gpioBcmNo)
    
    def output(self, gpioBcmNo, level):
        if level not in [self.levelHigh(), self.levelLow()]:
            raise RuntimeError("Paramter 'level' has an invalid value: %s" % str(level))
            
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



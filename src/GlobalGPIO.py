import RPi.GPIO as GPIO

class GlobalGPIO:
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        
    def __del__(self):
        GPIO.cleanup()

    def setup(self, gpioBcmNo, mode):
        GPIO.setup(gpioBcmNo, mode)
    
    def output(self, gpioBcmNo,level):
        GPIO.output(gpioBcmNo, level)
    
    def modeInput(self):
        return GPIO.IN
        
    def modeOutput(self):
        return GPIO.OUT

    def levelHigh(self):
        return GPIO.HIGH

    def levelLow(self):
        return GPIO.LOW



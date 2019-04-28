import RPi.GPIO as GPIO
from time import sleep

class GlobalGPIO:
    
    def __init__(self):
        self.usedOutputGPIOs = list()
        self.usedInputGPIOs = list()
        self.usedPwms = list()
        GPIO.setmode(GPIO.BCM)
        
    def __del__(self):
        for p in self.usedPwms:
            p.stop
        GPIO.cleanup()
        sleep(2)

    def setupOutput(self, gpioBcmNo):
        if gpioBcmNo in self.usedOutputGPIOs or gpioBcmNo in self.usedInputGPIOs:
            raise RuntimeError("GPIO %s already in use!" % str(gpioBcmNo))
            
        GPIO.setup(gpioBcmNo, GPIO.OUT)
        self.usedOutputGPIOs.append(gpioBcmNo)
    
    def setupInput(self, gpioBcmNo, pullUpDown=None):
        if gpioBcmNo in self.usedOutputGPIOs or gpioBcmNo in self.usedInputGPIOs:
            raise RuntimeError("GPIO %s already in use!" % str(gpioBcmNo))
            
        if pullUpDown not in [None, self.inputPullUp(), self.inputPullDown()]:
            raise RuntimeError("Invalid value for pull up/down: %s" % str(pullUpDown))
            
        if pullUpDown is None:
            GPIO.setup(gpioBcmNo, GPIO.IN)
        else:
            GPIO.setup(gpioBcmNo, GPIO.IN, pull_up_down=pullUpDown)
        self.usedInputGPIOs.append(gpioBcmNo)
    
    def output(self, gpioBcmNo, level):
        if level not in [self.levelHigh(), self.levelLow()]:
            raise RuntimeError("Parameter 'level' has an invalid value: %s" % str(level))
            
        if gpioBcmNo not in self.usedOutputGPIOs:
            raise RuntimeError("GPIO %s has not been set up as an output!" % str(gpioBcmNo))
            
        GPIO.output(gpioBcmNo, level) 
    
    def input(self, gpioBcmNo):
        if gpioBcmNo not in self.usedInputGPIOs:
            raise RuntimeError("GPIO %s has not been set up as an input!" % str(gpioBcmNo))
            
        return GPIO.input(gpioBcmNo)
        
    def pwm(self, gpioBcmNo, frequency):
        if gpioBcmNo not in self.usedOutputGPIOs:
            raise RuntimeError("GPIO %s has not been set up as an output!" % str(gpioBcmNo))
            
        p = GPIO.PWM(gpioBcmNo, frequency)
        self.usedPwms.append(p)
        return p

    def levelHigh(self):
        return GPIO.HIGH

    def levelLow(self):
        return GPIO.LOW

    def inputPullDown(self):
        return GPIO.PUD_DOWN
        
    def inputPullUp(self):
        return GPIO.PUD_UP

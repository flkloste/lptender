import pigpio
from time import sleep

class GlobalGPIO:
    
    class _Impl:
        def __init__(self):
            self.usedOutputGPIOs = list()
            self.usedInputGPIOs = list()
            self.usedPwms = list()

        def __enter__(self):
            self._pi = pigpio.pi()
            
        def __exit__(self):
            # stop all pwm output (servo)
            for p in self.usedPwms:
                p.stop
                self._pi.set_servo_pulsewidth(p, 0)
            
            self._pi.stop()

        def setupOutput(self, gpioBcmNo):
            if gpioBcmNo in self.usedOutputGPIOs or gpioBcmNo in self.usedInputGPIOs:
                raise RuntimeError("GPIO %s already in use!" % str(gpioBcmNo))
                
            #GPIO.setup(gpioBcmNo, GPIO.OUT)
            self._pi.set_mode(gpioBcmNo, pigpio.OUTPUT)
            self.usedOutputGPIOs.append(gpioBcmNo)
        
        def setupInput(self, gpioBcmNo, pullUpDown=None):
            if gpioBcmNo in self.usedOutputGPIOs or gpioBcmNo in self.usedInputGPIOs:
                raise RuntimeError("GPIO %s already in use!" % str(gpioBcmNo))
                
            if pullUpDown not in [None, self.inputPullUp(), self.inputPullDown()]:
                raise RuntimeError("Invalid value for pull up/down: %s" % str(pullUpDown))
                
            if pullUpDown is None:
                #GPIO.setup(gpioBcmNo, GPIO.IN)
                self._pi.set_mode(gpioBcmNo, pigpio.INPUT)
            else:
                #GPIO.setup(gpioBcmNo, GPIO.IN, pull_up_down=pullUpDown)
                self._pi.set_mode(gpioBcmNo, pigpio.INPUT)
                self._pi.set_pull_up_down(gpioBcmNo, pullUpDown)
            self.usedInputGPIOs.append(gpioBcmNo)
        
        def output(self, gpioBcmNo, level):
            if level not in [self.levelHigh(), self.levelLow()]:
                raise RuntimeError("Parameter 'level' has an invalid value: %s" % str(level))
                
            if gpioBcmNo not in self.usedOutputGPIOs:
                raise RuntimeError("GPIO %s has not been set up as an output!" % str(gpioBcmNo))
                
            #GPIO.output(gpioBcmNo, level) 
            self._pi.write(gpioBcmNo, level)
        
        def input(self, gpioBcmNo):
            if gpioBcmNo not in self.usedInputGPIOs:
                raise RuntimeError("GPIO %s has not been set up as an input!" % str(gpioBcmNo))
                
            #return GPIO.input(gpioBcmNo)
            return self._pi.read(gpioBcmNo)
            
    #    def pwm(self, gpioBcmNo, frequency):
    #        if gpioBcmNo not in self.usedOutputGPIOs:
    #            raise RuntimeError("GPIO %s has not been set up as an #output!" % str(gpioBcmNo))
    #            
    #        p = GPIO.PWM(gpioBcmNo, frequency)
    #        self.usedPwms.append(p)
    #        return p

        def setServoPulseWidth(self, gpioBcmNo, pulseWidth):
            if gpioBcmNo in self.usedOutputGPIOs or gpioBcmNo in self.usedInputGPIOs:
                raise RuntimeError("GPIO %s already in use!" % str(gpioBcmNo))
                
            if pulseWidth not in range(500, 2500) and pulseWidth != 0:
                raise RuntimeError("Invalid value for pulseWidth: %s" % str(pullUpDown))

            self._pi.set_servo_pulsewidth(gpioBcmNo, pulseWidth)
            
            if gpioBcmNo not in self.usedPwms:
                self.usedPwms.append(gpioBcmNo)

        def levelHigh(self):
            #return GPIO.HIGH
            return 1

        def levelLow(self):
            #return GPIO.LOW
            return 0

        def inputPullDown(self):
            #return GPIO.PUD_DOWN
            return pigpio.PUD_DOWN
            
        def inputPullUp(self):
            #return GPIO.PUD_UP
            return pigpio.PUD_UP

     # storage for the instance reference
    __instance = None  

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if GlobalGPIO.__instance is None:
            # Create and remember instance
            GlobalGPIO.__instance = GlobalGPIO._Impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_GlobalGPIO__instance'] = GlobalGPIO.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)

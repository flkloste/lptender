import pigpio

def checkContext(func):
    def decorator(self, *args, **kwargs):
        if self.contextCount == 0:  
             raise RuntimeError("Called out of context!")
        func(self, *args, **kwargs)
    return decorator

class GpioType:
    INPUT = 0
    OUTPUT = 1
    PWM = 2

class GlobalGPIO:
    
    class _Impl:
        def __init__(self):
            self.usedGPIOs = list()
            self.contextCount = 0

        def __enter__(self):
            if self.contextCount == 0:
                self._pi = pigpio.pi()
            self.contextCount += 1
            return self
            
        def __exit__(self, exc_type, exc_value, exc_traceback):
            self.contextCount -= 1
            
            if self.contextCount == 0:
                # stop all pwm output (servo)
                for pwmGpio in [gpio for (gpio, type) in self.usedGPIOs if type == GpioType.PWM]:
                    self._pi.set_servo_pulsewidth(pwmGpio, 0)
                
                del self.usedGPIOs[:]

                self._pi.stop()

        @checkContext
        def setupOutput(self, gpioBcmNo):
            if gpioBcmNo in [gpio for (gpio, type) in self.usedGPIOs]:
                raise RuntimeError("GPIO %s already in use!" % str(gpioBcmNo))
                
            self._pi.set_mode(gpioBcmNo, pigpio.OUTPUT)
            self.usedGPIOs.append((gpioBcmNo, GpioType.OUTPUT))
        
        @checkContext
        def setupInput(self, gpioBcmNo, pullUpDown=None):
            if gpioBcmNo in [gpio for (gpio, type) in self.usedGPIOs]:
                raise RuntimeError("GPIO %s already in use!" % str(gpioBcmNo))
                
            if pullUpDown not in [None, self.inputPullUp(), self.inputPullDown()]:
                raise RuntimeError("Invalid value for pull up/down: %s" % str(pullUpDown))
                
            if pullUpDown is None:
                self._pi.set_mode(gpioBcmNo, pigpio.INPUT)
            else:
                self._pi.set_mode(gpioBcmNo, pigpio.INPUT)
                self._pi.set_pull_up_down(gpioBcmNo, pullUpDown)
                
            self.usedGPIOs.append((gpioBcmNo, GpioType.INPUT))
        
        @checkContext
        def output(self, gpioBcmNo, level):
            if gpioBcmNo not in [gpio for (gpio, type) in self.usedGPIOs if type == GpioType.OUTPUT]:
                raise RuntimeError("GPIO %s has not been set up as an output!" % str(gpioBcmNo))

            if level not in [self.levelHigh(), self.levelLow()]:
                raise RuntimeError("Parameter 'level' has an invalid value: %s" % str(level))
                
            self._pi.write(gpioBcmNo, level)
        
        @checkContext
        def input(self, gpioBcmNo):
            if gpioBcmNo not in [gpio for (gpio, type) in self.usedGPIOs if type == GpioType.INPUT]:
                raise RuntimeError("GPIO %s has not been set up as an input!" % str(gpioBcmNo))
                
            return self._pi.read(gpioBcmNo)

        @checkContext
        def setServoPulseWidth(self, gpioBcmNo, pulseWidth):
            if gpioBcmNo in [gpio for (gpio, type) in self.usedGPIOs if (type in [GpioType.INPUT, GpioType.OUTPUT])]:
                raise RuntimeError("GPIO %s already in use!" % str(gpioBcmNo))
                
            if pulseWidth not in range(500, 2500) and pulseWidth != 0:
                raise RuntimeError("Invalid value for pulseWidth: %s" % str(pullUpDown))

            self._pi.set_servo_pulsewidth(gpioBcmNo, pulseWidth)
            
            if gpioBcmNo not in [gpio for (gpio, type) in self.usedGPIOs]:
                self.usedGPIOs.append((gpioBcmNo, GpioType.PWM))

        def levelHigh(self):
            return 1

        def levelLow(self):
            return 0

        def inputPullDown(self):
            return pigpio.PUD_DOWN
            
        def inputPullUp(self):
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

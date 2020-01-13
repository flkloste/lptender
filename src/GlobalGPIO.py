import pigpio

def checkContext(func):
    def decorator(self, *args, **kwargs):
        if self._contextCount == 0:  
             raise RuntimeError("Called out of context!")
        return func(self, *args, **kwargs)
    return decorator

class GpioType:
    INPUT = 0
    OUTPUT = 1
    PWM = 2

class GlobalGPIO:
    
    class _Impl:
        def __init__(self):
            self._usedGPIOs = list()
            self._contextCount = 0

        def __enter__(self):
            if self._contextCount == 0:
                self._pi = pigpio.pi()
            self._contextCount += 1
            return self
            
        def __exit__(self, exc_type, exc_value, exc_traceback):
            self._contextCount -= 1
            
            if self._contextCount == 0:
                # stop all pwm output (servo)
                for pwmGpio in [gpio for (gpio, type) in self._usedGPIOs if type == GpioType.PWM]:
                    self._pi.set_servo_pulsewidth(pwmGpio, 0)
                
                del self._usedGPIOs[:]

                self._pi.stop()

        @checkContext
        def setupOutput(self, gpioBcmNo):
            if gpioBcmNo in [gpio for (gpio, type) in self._usedGPIOs]:
                raise RuntimeError("GPIO %s already in use!" % str(gpioBcmNo))
                
            self._pi.set_mode(gpioBcmNo, pigpio.OUTPUT)
            self._usedGPIOs.append((gpioBcmNo, GpioType.OUTPUT))
        
        @checkContext
        def setupInput(self, gpioBcmNo, pullUpDown=None):
            if gpioBcmNo in [gpio for (gpio, type) in self._usedGPIOs]:
                raise RuntimeError("GPIO %s already in use!" % str(gpioBcmNo))
                
            if pullUpDown not in [None, self.inputPullUp(), self.inputPullDown()]:
                raise RuntimeError("Invalid value for pull up/down: %s" % str(pullUpDown))
                
            if pullUpDown is None:
                self._pi.set_mode(gpioBcmNo, pigpio.INPUT)
            else:
                self._pi.set_mode(gpioBcmNo, pigpio.INPUT)
                self._pi.set_pull_up_down(gpioBcmNo, pullUpDown)
                
            self._usedGPIOs.append((gpioBcmNo, GpioType.INPUT))
        
        @checkContext
        def output(self, gpioBcmNo, level):
            if gpioBcmNo not in [gpio for (gpio, type) in self._usedGPIOs if type == GpioType.OUTPUT]:
                raise RuntimeError("GPIO %s has not been set up as an output!" % str(gpioBcmNo))

            if level not in [self.levelHigh(), self.levelLow()]:
                raise RuntimeError("Parameter 'level' has an invalid value: %s" % str(level))
                
            self._pi.write(gpioBcmNo, level)
        
        @checkContext
        def input(self, gpioBcmNo):
            if gpioBcmNo not in [gpio for (gpio, type) in self._usedGPIOs if type == GpioType.INPUT]:
                raise RuntimeError("GPIO %s has not been set up as an input!" % str(gpioBcmNo))
                
            return self._pi.read(gpioBcmNo)

        @checkContext
        def setServoPulseWidth(self, gpioBcmNo, pulseWidth):
            if gpioBcmNo in [gpio for (gpio, type) in self._usedGPIOs if (type in [GpioType.INPUT, GpioType.OUTPUT])]:
                raise RuntimeError("GPIO %s already in use!" % str(gpioBcmNo))
                
            if pulseWidth not in range(500, 2500) and pulseWidth != 0:
                raise RuntimeError("Invalid value for pulseWidth: %s" % str(pullUpDown))

            self._pi.set_servo_pulsewidth(gpioBcmNo, pulseWidth)
            
            if gpioBcmNo not in [gpio for (gpio, type) in self._usedGPIOs]:
                self._usedGPIOs.append((gpioBcmNo, GpioType.PWM))

        @checkContext
        def setPwm(self, gpioBcmNo, dutycycle, frequency):
            if gpioBcmNo not in [gpio for (gpio, type) in self._usedGPIOs if type == GpioType.OUTPUT]:
                raise RuntimeError("GPIO %s has not been set up as an output!" % str(gpioBcmNo))

            self._pi.set_PWM_dutycycle(gpioBcmNo, dutycycle) 
            self._pi.set_PWM_frequency(gpioBcmNo, frequency)

        @checkContext
        def stopPwm(self, gpioBcmNo):
            if gpioBcmNo not in [gpio for (gpio, type) in self._usedGPIOs if type == GpioType.OUTPUT]:
                raise RuntimeError("GPIO %s has not been set up as an output!" % str(gpioBcmNo))

            self._pi.set_PWM_dutycycle(gpioBcmNo, 0)

        def levelHigh(self):
            return 1

        def levelLow(self):
            return 0

        def inputPullDown(self):
            return pigpio.PUD_DOWN
            
        def inputPullUp(self):
            return pigpio.PUD_UP

        @checkContext
        def generate_ramp(self, ramp, step_gpio):
            """Generate ramp wave forms.
            https://www.rototron.info/raspberry-pi-stepper-motor-tutorial/
            ramp:  List of [Frequency, Steps]
            """
            self._pi.wave_clear()     # clear existing waves
            length = len(ramp)  # number of ramp levels
            wid = [-1] * length

            # Generate a wave per ramp level
            for i in range(length):
                frequency = ramp[i][0]
                micros = int(500000 / frequency)
                wf = []
                wf.append(pigpio.pulse(1 << step_gpio, 0, micros))  # pulse on
                wf.append(pigpio.pulse(0, 1 << step_gpio, micros))  # pulse off
                self._pi.wave_add_generic(wf)
                wid[i] = self._pi.wave_create()

            # Generate a chain of waves
            chain = []
            for i in range(length):
                steps = ramp[i][1]
                x = steps & 255
                y = steps >> 8
                chain += [255, 0, wid[i], 255, 1, x, y]

            self._pi.wave_chain(chain)  # Transmit chain.

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

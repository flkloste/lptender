from time import sleep

class RecordPlayer:

    def __init__(self, gpioController, gpioStart, gpioStop, gpioLightBarrier):
        self._gpioController = gpioController
        self._gpioStart = gpioStart
        self._gpioStop = gpioStop
        self._gpioLightBarrier = gpioLightBarrier

        self._gpioController.setupInput(self._gpioLightBarrier, self._gpioController.inputPullDown())
        self._gpioController.setupOutput(self._gpioStart)
        self._gpioController.setupOutput(self._gpioStop)


    def start(self):
        self._gpioController.output(self._gpioStart, self._gpioController.levelHigh())
        sleep(1)
        self._gpioController.output(self._gpioStart, self._gpioController.levelLow())
        
        # wait until tonearm has left
        timeoutCount = 0
        while self._gpioController.input(self._gpioLightBarrier) != self._gpioController.levelLow():
            timeoutCount += 1

            # if tonearm hasn't left after 15 secs, there's something wrong
            if timeoutCount > 15:
                raise RuntimeError("Timeout")
            else:
                # after tonearm has left, give it 10 more seconds to settle on the lp
                sleep(10)


    def stop(self):
        self._gpioController.output(self._gpioStop, self._gpioController.levelHigh())
        sleep(1)
        self._gpioController.output(self._gpioStop, self._gpioController.levelLow())


    def waitUntilStopped(self):
        while self._gpioController.input(self._gpioLightBarrier) != self._gpioController.levelHigh():
            sleep(1)
        
        # give it some more time to settle after tonearm is returned
        sleep(5)


    def isStopped(self):
        return self._gpioController.input(self._gpioLightBarrier) == self._gpioController.levelHigh()
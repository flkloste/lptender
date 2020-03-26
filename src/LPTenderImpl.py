import Elevator
import Servo
import GlobalGPIO
from time import sleep


class LpTenderMock(object):
    def __init__(gpioController, config):
        self._gpioController  = gpioController
        self._config = config
        self._elevator = Elevator.Elevator(self._config, self._gpioController)
        self._gripper = Gripper.Gripper(gpio)
    def initialize(self):
        raise 1
    def pressPlay(self):
        raise 1
    def waitForPlaying(self):
        raise 1    
    def stop(self):
        raise 1        
    def waitForEndOfRecord(self):
        raise 1
    def flip(self):
        raise 1
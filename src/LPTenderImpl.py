import Elevator
import Servo
import GlobalGPIO
from time import sleep


class LpTenderMock(object):
    def __init__(gpioController, config):
        self._gpioController  = gpioController
        self._config = config
        self._elevator = Elevator.Elevator(self._config, self._gpioController)
        self._gripper = Gripper.Gripper(gpioController, config)
        self._servoRotate = Servo.ServoDS3218_270(gpio, self._config.servo_rotate.gpio)

    def initialize(self):
        self._gripper.release()
        self._elevator.gotoHome()
        
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
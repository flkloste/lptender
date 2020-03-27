import Elevator
import Servo
import GlobalGPIO
import RecordPlayer
from time import sleep


class LpTenderImpl(object):

    class ElevatorPosition:
        HOME = 1
        RECORD_PLAYER = 2

    class ServoRotatePosition:
        BASE = 1
        FLIPPED = 2

    def __init__(gpioController, config):
        self._gpioController  = gpioController
        self._config = config
        self._elevator = Elevator.Elevator(self._config, self._gpioController)
        self._gripper = Gripper.Gripper(self._gpioController, self._config)
        self._servoRotate = Servo.ServoDS3218_270(self._gpioController, self._config.servo_rotate.gpio)
        self._recordPlayer = RecordPlayer.RecordPlayer(self._gpioController, self._config.record_player.gpio_start, self._config.record_player.gpio_stop, self._config.record_player.gpio_light_barrier)
        self._currentElevatorPosition = None
        self._currentServoRotatePosition = None

        self.ROTATE_0 = self._config.servo_rotate.rotate_0
        self.ROTATE_180 = self._config.servo_rotate.rotate_180

        self.HOME_TO_BASE = self._config.elevator.home_to_base
        self.FLIPPED_DELTA = self._config.elevator.flipped_delta

    def initialize(self):
        self._gripper.release()
        self._elevator.gotoHome()
        self._servo_rotate.setAngle(self.ROTATE_0)
        sleep(2)
        servo_rotate.dontMove()
        self._currentServoRotatePosition = LpTenderImpl.ServoRotatePosition.BASE
        self._elevator.moveDown(self.HOME_TO_BASE)
        self._currentPosition = LpTenderImpl.ElevatorPosition.RECORD_PLAYER
        sleep(1)
        
    def pressPlay(self):
        self._recordPlayer.start()

    def waitForPlaying(self):
        sleep(15)

    def stop(self):
        self._recordPlayer.stop()
        self._recordPlayer.waitUntilStopped()

    def waitForEndOfRecord(self):
        self._recordPlayer.waitUntilStopped()

    def flip(self):
        if self._currentPosition != 
import Elevator
import Servo
import GlobalGPIO
import RecordPlayer
from time import sleep
from threading import Lock

def checkInitialized(func):
    def funcWrap(self, *args, **kwargs):
        if not self._ready:
            raise RuntimeError("Lptender is not initialized!")
            func(*args, **kwargs)    
    return funcWrap

class LpTenderImpl(object):

    def __init__(gpioController, config):
        self._gpioController  = gpioController
        self._config = config
        self._elevator = Elevator.Elevator(self._config, self._gpioController)
        self._gripper = Gripper.Gripper(self._gpioController, self._config)
        self._servoRotate = Servo.ServoDS3218_270(self._gpioController, self._config.servo_rotate.gpio)
        self._recordPlayer = RecordPlayer.RecordPlayer(self._gpioController, self._config.record_player.gpio_start, self._config.record_player.gpio_stop, self._config.record_player.gpio_light_barrier)

        self._lock = Lock()
        self._ready = False

        self.ROTATE_0 = self._config.servo_rotate.rotate_0
        self.ROTATE_180 = self._config.servo_rotate.rotate_180

        self.HOME_TO_BASE = self._config.elevator.home_to_base
        self.FLIPPED_DELTA = self._config.elevator.flipped_delta

    def initialize(self):
        if self._ready:
            raise RuntimeError("Is already initialized!")

        with self._lock:
            self._gripper.release()
            self._elevator.gotoHome()

            self._servo_rotate.setAngle(self.ROTATE_0)
            sleep(2)
            self._servo_rotate.dontMove()

            self._elevator.moveDown(self.HOME_TO_BASE)
            sleep(1)
            self._ready = True
        
    @checkInitialized
    def pressPlay(self):
        with self._lock:
            self._recordPlayer.start()

    @checkInitialized
    def waitForPlaying(self):
        sleep(15)

    @checkInitialized
    def stop(self):
        with self._lock:
            self._recordPlayer.stop()
            self._recordPlayer.waitUntilStopped()

    @checkInitialized
    def waitForEndOfRecord(self):
        self._recordPlayer.waitUntilStopped()

    @checkInitialized
    def flip(self):
        if not self._recordPlayer.isStopped():
            raise RuntimeError("Cannot flip: Is not stopped!")

        with self._lock:
            self._gripper.grip()
            sleep(2)
            self._elevator.gotoHome()

            self._servoRotate.setAngle(self.ROTATE_180)
            sleep(2)
            self._servoRotate.dontMove()

            self._elevator.moveDown(self.HOME_TO_BASE - self.FLIPPED_DELTA)
            sleep(1)
            self._gripper.release()
            sleep(1)

            self._elevator.gotoHome()
            self._servoRotate.setAngle(self.ROTATE_0)
            sleep(2)
            self._servoRotate.dontMove()

            self._elevator.moveDown(self.HOME_TO_BASE)
            sleep(1)

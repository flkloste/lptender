import Servo
from time import sleep

class Gripper:
    def __init__(self, globalGPIO):
        self._gpioLeftServoControl = XX
        self._gpioRightServoControl = XX
        self._leftServo = Servo.ServoDS3218_180(globalGPIO, _gpioLeftServoControl)
        self._rightServo = Servo.ServoDS3218_180(globalGPIO, _gpioRightServoControl)
        self._rightServoCloseAngle = 100       
        self._rightServoOpenAngle = 80
        self._leftServoCloseAngle = 80
        self._leftServoOpenAngle = 100
        
    def grip(self):
        self._leftServo.setAngle(_leftServoCloseAngle)
        self._rightServo.setAngle(_rightServoCloseAngle)
        sleep(1)
        servo.dontMove()
        
    def release(self):
        self._leftServo.setAngle(_leftServoOpenAngle)
        self._rightServo.setAngle(_rightServoOpenAngle)
        sleep(1)
        servo.dontMove()
        
    
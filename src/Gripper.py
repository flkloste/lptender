import Servo
from time import sleep

class Gripper:
    def __init__(self, globalGPIO):
        self._gpioLeftServoControl = 27
        self._gpioRightServoControl = 22
        self._leftServo = Servo.ServoDS3218_180(globalGPIO, self._gpioLeftServoControl)
        self._rightServo = Servo.ServoDS3218_180(globalGPIO, self._gpioRightServoControl)
        self._rightServoCloseAngle = 103
        self._rightServoOpenAngle = 95
        self._leftServoCloseAngle = 72 
        self._leftServoOpenAngle = 80 
        
    def grip(self):
        self._leftServo.setAngle(self._leftServoCloseAngle)
        self._rightServo.setAngle(self._rightServoCloseAngle)
        sleep(1)
        self._leftServo.dontMove()
        self._rightServo.dontMove()
        
    def release(self):
        self._leftServo.setAngle(self._leftServoOpenAngle)
        self._rightServo.setAngle(self._rightServoOpenAngle)
        sleep(1)
        self._leftServo.dontMove()
        self._rightServo.dontMove()
        
    

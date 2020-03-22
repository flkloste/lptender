import Servo
from time import sleep

class Gripper:
    def __init__(self, globalGPIO):
        self._gpioLeftServoControl = 27
        self._gpioRightServoControl = 22
        self._leftServo = Servo.ServoDS3218_180(globalGPIO, self._gpioLeftServoControl)
        self._rightServo = Servo.ServoDS3218_180(globalGPIO, self._gpioRightServoControl)
        self._rightServoCloseAngle = 106
        self._rightServoOpenAngle = 99
        self._rightServoCurrentAngle = -1
        self._leftServoCloseAngle = 73 
        self._leftServoOpenAngle = 79
        self._leftServoCurrentAngle = -1

        
    def grip(self):
        if ( self._leftServoCurrentAngle < 0 
             or self._rightServoCurrentAngle < 0
             or self._leftServoCurrentAngle < self._leftServoCloseAngle
             or self._rightServoCurrentAngle > self._rightServoCloseAngle ):
            self._leftServo.setAngle(self._leftServoCloseAngle)
            self._rightServo.setAngle(self._rightServoCloseAngle)
            self._leftServoCurrentAngle = self._leftServoCloseAngle
            self._rightServoCurrentAngle = self._rightServoCloseAngle
        else:
            for i in range(max((self._rightServoCloseAngle - self._rightServoCurrentAngle), (self._leftServoCurrentAngle - self._leftServoCloseAngle))*2):
                if(self._leftServoCurrentAngle > self._leftServoCloseAngle):
                    self._leftServoCurrentAngle -= 0.5
                    self._leftServo.setAngle(self._leftServoCurrentAngle)
                if(self._rightServoCurrentAngle < self._rightServoCloseAngle):
                    self._rightServoCurrentAngle += 0.5
                    self._rightServo.setAngle(self._rightServoCurrentAngle)
                sleep(0.1)

        sleep(1)
        self._leftServo.dontMove()
        self._rightServo.dontMove()
        
    def release(self):
        self._leftServo.setAngle(self._leftServoOpenAngle)
        self._rightServo.setAngle(self._rightServoOpenAngle)
        sleep(1)
        self._leftServo.dontMove()
        self._rightServo.dontMove()
        self._leftServoCurrentAngle = self._leftServoOpenAngle
        self._rightServoCurrentAngle = self._rightServoOpenAngle
        
    

import Elevator
import Servo
import GlobalGPIO
from time import sleep
from random import randint

if __name__ == "__main__":
    gpio = GlobalGPIO.GlobalGPIO()
    elevator = Elevator.Elevator(gpio)
    servo_rotate = Servo.ServoDS3218_270(gpio, 17)
    servo_left = Servo.ServoDS3218_180(gpio, 27)
    servo_right = Servo.ServoDS3218_180(gpio, 22)

    servo_rotate.setAngle(182)
    sleep(2)
    servo_rotate.dontMove()
   
    elevator.gotoHome()
    elevator.moveDown(20000)
    elevator.moveUp(15000)

    sleep(2) 
    servo_rotate.setAngle(9)
    sleep(2)
    servo_rotate.dontMove()
   
    sleep(2)
    servo_rotate.setAngle(182)
    sleep(2)
    servo_rotate.dontMove()
    sleep(2)
   
    # release LP
    servo_left.setAngle(100)
    servo_right.setAngle(80)
    sleep(1)
    servo_left.dontMove()
    servo_right.dontMove()

    sleep(5)

    # grap LP
    servo_left.setAngle(80)
    servo_right.setAngle(100)
    sleep(1)
    servo_left.dontMove()
    servo_right.dontMove()

    sleep(2)


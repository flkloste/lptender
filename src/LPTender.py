import Elevator
import Servo
import GlobalGPIO
from time import sleep


if __name__ == "__main__":
    gpio = GlobalGPIO.GlobalGPIO()
    #elevator = Elevator.Elevator(gpio)

    #elevator.gotoHome()
    #elevator.moveDown(20000)
    #sleep(1)
    #elevator.moveUp(10000)
    
    servo = Servo.Servo(gpio, 17)
    servo.setAngle(90)
    sleep(1)
    servo.dontMove()
    sleep(1)
    servo.setAngle(100)
    sleeo(1)
    servo.dontMove()

import Elevator
import Servo
import GlobalGPIO
from time import sleep


if __name__ == "__main__":
    gpio = GlobalGPIO.GlobalGPIO()
    elevator = Elevator.Elevator(gpio)
    servo = Servo.Servo(gpio, 17)
    servo.setAngle(70)
    sleep(0.5)
    servo.dontMove()
    sleep(10)
    servo.setAngle(86)
    sleep(0.5)
    servo.dontMove()

    elevator.gotoHome()
    elevator.moveDown(20000)
    
    elevator.moveUp(10000)
    

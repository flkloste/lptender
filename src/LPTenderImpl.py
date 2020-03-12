import Elevator
import Servo
import GlobalGPIO
from time import sleep


if __name__ == "__main__":
    gpio = GlobalGPIO.GlobalGPIO()
    #elevator = Elevator.Elevator(gpio)
    
    servo = Servo.ServoDS3218_180(gpio, 17)
    
    servo.setAngle(65)
    sleep(1)
    servo.dontMove()

    sleep(1)
    servo.setAngle(85)
    sleep(1)
    servo.dontMove()
    sleep(1) 
    #elevator.gotoHome()
    #elevator.moveDown(20000)
    
    #elevator.moveUp(10000)
    

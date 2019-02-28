import Elevator
import Servo
import GlobalGPIO
from time import sleep


if __name__ == "__main__":
    gpio = GlobalGPIO.GlobalGPIO()
    #elevator = Elevator.Elevator(gpio)
    
    servo = Servo.ServoDS3218_180(gpio, 17)
    
    for i in range (1,100):
        servo.setAngle(2 + float(i)/100)
        sleep(0.5)
    
    #elevator.gotoHome()
    #elevator.moveDown(20000)
    
    #elevator.moveUp(10000)
    

import Elevator
import GlobalGPIO
from time import sleep


if __name__ == "__main__":
    gpio = GlobalGPIO.GlobalGPIO()
    elevator = Elevator.Elevator(gpio)

    elevator.gotoHome()
    elevator.moveDown(20000)
    sleep(1)
    elevator.moveUp(10000)
    

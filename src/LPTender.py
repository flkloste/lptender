import Elevator
import GlobalGPIO
from time import sleep


if __name__ == "__main__":
    gpio = GlobalGPIO()
    elevator = Elevator(gpio)
    
    elevator.moveUp(200)
    sleep(1)
    elevator.moveDown(200)
    
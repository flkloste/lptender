import Elevator
import Servo
import GlobalGPIO
import Gripper
from time import sleep
import LPTenderMock
from LPTenderStateMachine import LpTenderStateMachine
from LPTenderStateMachine import Transitions

from GlobalConfig import GlobalConfig

if __name__ == "__main__":
 
    #config = GlobalConfig()
    #print config.elevator.gpioEndstopSignal
    
    lptender = LPTenderMock.LpTenderMock()
    lpTenderFSM = LpTenderStateMachine(lptender)

    print lpTenderFSM.getCurrentState()
    lpTenderFSM.doTransition(Transitions.FlipWithAutoplay)
    sleep(4)
    lpTenderFSM.doTransition(Transitions.Stop)
    sleep(2)
    lpTenderFSM.doTransition(Transitions.Stop)

    sleep(4)


"""
    with GlobalGPIO.GlobalGPIO() as gpio:
        elevator = Elevator.Elevator(gpio)
        servo_rotate = Servo.ServoDS3218_270(gpio, 17)
        gripper = Gripper.Gripper(gpio)
        ROTATE_0 = 179
        ROTATE_180 = 2
        HOME_TO_BASE = 34000
        FLIPPED_DELTA = 4600
        
        gripper.release()
        elevator.gotoHome()
        servo_rotate.setAngle(ROTATE_0)
        sleep(5)
        elevator.moveDown(HOME_TO_BASE)
        sleep(2)
        gripper.grip()

        elevator.gotoHome()
        servo_rotate.setAngle(ROTATE_180)
        sleep(4)
        elevator.moveDown(HOME_TO_BASE - FLIPPED_DELTA)
        gripper.release()
        sleep(3)
"""
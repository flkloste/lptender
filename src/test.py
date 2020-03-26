import Elevator
import Servo
import GlobalGPIO
import Gripper
from time import sleep
import LPTenderMock
from LPTenderStateMachine import States
from LPTenderStateMachine import LpTenderStateMachine
from LPTenderStateMachine import Transitions

from GlobalConfig import GlobalConfig

if __name__ == "__main__":
    
    config = GlobalConfig()

    with GlobalGPIO.GlobalGPIO() as gpio:
        gripper = Gripper.Gripper(gpio, config)
        gripper.release() 
        sleep(2)
     #   gripper.grip()
     #   sleep(2)
    #    gripper.release()
        
        elevator = Elevator.Elevator(config, gpio)

        elevator.gotoHome()

        HOME_TO_BASE = 100000
        FLIPPED_DELTA = 18000

        servo_rotate = Servo.ServoDS3218_270(gpio, 17)
       
      #  gripper.grip()

        ROTATE_0 = 180
        ROTATE_180 = 5

        # slowly
      
      #  servo_rotate.setAngle(ROTATE_180)
      #  sleep(3)
        servo_rotate.setAngle(ROTATE_0)
      #  sleep(3)
      
      #  sleep(3)
     #   servo_rotate.setAngle(ROTATE_180)
      

        sleep(2)
        servo_rotate.dontMove()
      #  gripper.release()
        elevator.moveDown(HOME_TO_BASE)
       


        sleep(2)
        
  #      elevator.moveDown(HOME_TO_BASE)

     #   sleep(1)

        gripper.grip()

        sleep(2)

        elevator.gotoHome()

        servo_rotate.setAngle(ROTATE_180)
        sleep(2)
        servo_rotate.dontMove()

        elevator.moveDown(HOME_TO_BASE - FLIPPED_DELTA)
        sleep(2)
        gripper.release()

        #elevator.gotoHome()
        #servo_rotate.setAngle(ROTATE_180)
        #sleep(4)
        #elevator.moveDown(HOME_TO_BASE - FLIPPED_DELTA)
        #gripper.release()
        sleep(3)

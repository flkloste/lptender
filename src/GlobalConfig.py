class GlobalConfig(object):

    class Elevator(object):
        def __init__(self):
            self._gpioStep = 21
            self._gpioDirection = 20
            self._gpioEndstopSignal = 4
        
        @property
        def gpioStep(self):
            return self._gpioStep

        @property
        def gpioDirection(self):
            return self._gpioDirection

        @property
        def gpioEndstopSignal(self):
            return self._gpioEndstopSignal

    class Gripper(object):
        def __init__(self):
            self._gpioLeftServoControl = 27
            self._gpioRightServoControl = 22
            self._rightServoCloseAngle = 106
            self._rightServoOpenAngle = 99
            self._leftServoCloseAngle = 73
            self._leftServoOpenAngle = 79

        @property
        def gpioLeftServoControl(self):
            return self._gpioLeftServoControl

        @property
        def gpioRightServoControl(self):
            return self._gpioRightServoControl

        @property
        def rightServoCloseAngle(self):
            return self._rightServoCloseAngle

        @property
        def rightServoOpenAngle(self):
            return self._rightServoOpenAngle

        @property
        def leftServoCloseAngle(self):
            return self._leftServoCloseAngle

        @property
        def leftServoOpenAngle(self):
            return self._leftServoOpenAngle
        
    def __init__(self):
        self._elevator = GlobalConfig.Elevator()
        self._gripper = GlobalConfig.Gripper()

    @property
    def elevator(self):
        return self._elevator

    @property
    def gripper(self):
        return self._gripper


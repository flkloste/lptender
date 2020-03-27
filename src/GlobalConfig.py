class GlobalConfig(object):

    class Elevator(object):
        def __init__(self):
            self._gpioStep = 21
            self._gpioDirection = 20
            self._gpioEndstopSignal = 4
            self._home_to_base = 100000
            self._flipped_delta = 18000
        
        @property
        def gpioStep(self):
            return self._gpioStep

        @property
        def gpioDirection(self):
            return self._gpioDirection

        @property
        def gpioEndstopSignal(self):
            return self._gpioEndstopSignal

        @property
        def home_to_base(self):
            return self._home_to_base

        @property
        def flipped_delta(self):
            return self._flipped_delta

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

    class ServoRotate(object):
        def __init__(self):
            self._gpio = 17
            self._rotate_0 = 180
            self._rotate_180 = 5

        @property
        def gpio(self):
            return self._gpio

        @property
        def rotate_0(self):
            return self._rotate_0

        @property
        def rotate_180(self):
            return self._rotate_180

    class RecordPlayer(object):
        def __init__(self):
            self._gpio_start = 14
            self._gpio_stop = 15
            self._gpio_light_barrier = 18

        @property
        def gpio_start(self):
            return self._gpio_start

        @property
        def gpio_stop(self):
            return self._gpio_stop
        
        @property
        def gpio_light_barrier(self):
            return self._gpio_light_barrier

    def __init__(self):
        self._elevator = GlobalConfig.Elevator()
        self._gripper = GlobalConfig.Gripper()
        self._servo_rotate = GlobalConfig.ServoRotate()
        self._record_player = GlobalConfig.RecordPlayer()

    @property
    def elevator(self):
        return self._elevator

    @property
    def gripper(self):
        return self._gripper

    @property
    def servo_rotate(self):
        return self._servo_rotate

    @property
    def record_player(self):
        return self._record_player
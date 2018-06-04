class Rotation_Motor(object):
    def __init__(self, controller):
        self._controller = controller
        self._direction = 1
        self._position = 0
        self._speed = None
        self._acceleration = None

    def move_left(self, steps):
        self._position += steps * -1
        self._controller.send_command("G1X" + str(self._position))

    def move_right(self, steps):
        self._position += steps
        self._controller.send_command("G1X" + str(self._position))

    def move_to_position(self, position):
        self._position = position * -1
        self._controller.send_command("G1X" + str(self._position))

    def motor_speed(self, speed):
        self._speed = speed
        self._controller.send_command("G1F" + str(speed))

    def motor_acceleration(self, acceleration):
        self._acceleration = acceleration
        self._controller.send_command("$120=" + str(acceleration))

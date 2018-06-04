import controller_driver
import laser_driver
import table_motor_driver
import rotation_motor_driver
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class HW_Interface():
    def __init__(self, serial_name='/dev/ttyUSB0', baud_rate=115200):

        #Create Controller Object
        self._controller = controller_driver.Controller(serial_name=serial_name, baud_rate=baud_rate)

        # Create Laser Objects
        self.Laser_Right = laser_driver.Laser(self._controller, 1)
        self.Laser_Left = laser_driver.Laser(self._controller, 2)

        # Create Table Motor Object
        self.Table_Motor = table_motor_driver.Table_Motor(self._controller)

    def connect(self):
        self._controller.connect()

    def disconnect(self):
        del self._controller

    def motor_invert(self, value):
        self._controller.Table_Motor.invert_direction()

    def motor_acceleration(self, value):
        if self._controller.connected:
            self._controller.Table_Motor.acceleration = value

    def motor_speed(self, value):
        if self._controller.connected:
            self._controller.Table_Motor.speed = speed

    def motor_reset_origin(self):
        if self._controller.connected:
            self._controller.Table_Motor.move_to_position(0)

    def motor_move(self, step=0):
        if self._controller.connected:
            self._controller.Table_Motor.move(step)

    def laser_on(self, index):
        if self._controller.connected:
            if index is 0:
                self._controller.Laser_Left.on()
            else:
                self._controller.Laser_Right.on()

    def laser_off(self, index):
        if self._controller.connected:
            if index is 0:
                self._controller.Laser_Left.off()
            else:
                self._controller.Laser_Right.off()

    def lasers_on(self):
        if self._controller.connected:
            self._controller.Laser_Left.on()
            self._controller.Laser_Right.on()


    def lasers_off(self):
        if self._controller.connected:
            self._controller.Laser_Left.off()
            self._controller.Laser_Right.off()

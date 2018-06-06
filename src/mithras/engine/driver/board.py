# -*- coding: utf-8 -*-
# This file is part of the Horus Project

__author__ = 'Jesús Arroyo Torrens <jesus.arroyo@bq.com>'
__copyright__ = 'Copyright (C) 2014-2016 Mundo Reader S.L.'
__license__ = 'GNU General Public License v2 http://www.gnu.org/licenses/gpl2.html'

import time
import glob
import serial
import threading
import platform
import controller_driver
import laser_driver
import table_motor_driver
import rotation_motor_driver
import logging

import logging
logger = logging.getLogger(__name__)

system = platform.system()


class WrongFirmware(Exception):

    def __init__(self):
        Exception.__init__(self, "Wrong Firmware")


class BoardNotConnected(Exception):

    def __init__(self):
        Exception.__init__(self, "Board Not Connected")


class OldFirmware(Exception):

    def __init__(self):
        Exception.__init__(self, "Old Firmware")


class Board(object):

    """Board class. For accessing to the scanner board

    Gcode commands:

        G1 Fnnn : feed rate
        G1 Xnnn : move motor
        G50     : reset origin position

        M70 Tn  : switch off laser n
        M71 Tn  : switch on laser n

        M50 Tn  : read ldr sensor

    """

    def __init__(self, parent=None, serial_name='/dev/ttyUSB0', baud_rate=115200):
                #Create Controller Object
        self._controller = controller_driver.Controller(serial_name=serial_name, baud_rate=baud_rate)

        # Create Laser Objects
        self.Laser_Right = laser_driver.Laser(self._controller, 1)
        self.Laser_Left = laser_driver.Laser(self._controller, 2)

        # Create Table Motor Object
        self.Table_Motor = table_motor_driver.Table_Motor(self._controller)
        self.serial_name = serial_name
        self.baud_rate = baud_rate
        self.unplug_callback = None
        self._serial_port = None
        self._is_connected = False
        self._motor_enabled = False
        self._tries = 0  # Check if command fails

    def connect(self):
        self._controller.connect()
        self._is_connected = True

    def disconnect(self):
        del self._controller
        self._is_connected = False

    def set_unplug_callback(self, value):
        self.unplug_callback = value

    def motor_invert(self, value):
        self._controller.Table_Motor.invert_direction()

    def motor_speed(self, value):
        if self._controller.connected:
            self._controller.Table_Motor.speed = speed

    def motor_acceleration(self, value):
        if self._controller.connected:
            self._controller.Table_Motor.acceleration = value

    def motor_enable(self):
        if self._controller.connected:
            pass

    def motor_disable(self):
        if self._controller.connected:
            pass

    def motor_reset_origin(self):
        if self._controller.connected:
            self._controller.Table_Motor.move_to_position(0)

    def motor_move(self, step=0, nonblocking=False, callback=None):
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

    def ldr_sensor(self, pin):
        value = self._send_command("M50T" + pin, read_lines=True).split("\n")[0]
        try:
            return int(value)
        except ValueError:
            return 0

    def send_command(self, req, nonblocking=False, callback=None, read_lines=False):
        if nonblocking:
            threading.Thread(target=self._send_command,
                             args=(req, callback, read_lines)).start()
        else:
            self._send_command(req, callback, read_lines)

    def _send_command(self, req, callback=None, read_lines=False):
        """Sends the request and returns the response"""
        ret = ''
        if self._is_connected and req != '':
            if self._serial_port is not None and self._serial_port.isOpen():
                try:
                    self._serial_port.flushInput()
                    self._serial_port.flushOutput()
                    self._serial_port.write(req + "\r\n")
                    while req != '~' and req != '!' and ret == '':
                        ret = self.read(read_lines)
                        time.sleep(0.01)
                    self._success()
                except:
                    if hasattr(self, '_serial_port'):
                        if callback is not None:
                            callback(ret)
                        self._fail()
        if callback is not None:
            callback(ret)
        return ret

    def read(self, read_lines=False):
        if read_lines:
            return ''.join(self._serial_port.readlines())
        else:
            return ''.join(self._serial_port.readline())

    def _success(self):
        self._tries = 0

    def _fail(self):
        if self._is_connected:
            logger.debug("Board fail")
            self._tries += 1
            if self._tries >= 3:
                self._tries = 0
                if self.unplug_callback is not None and \
                   self.parent is not None and \
                   not self.parent.unplugged:
                    self.parent.unplugged = True
                    self.unplug_callback()

    def _reset(self):
        self._serial_port.flushInput()
        self._serial_port.flushOutput()
        self._serial_port.write("\x18\r\n")  # Ctrl-x
        self._serial_port.readline()

    def get_serial_list(self):
        """Obtain list of serial devices"""
        baselist = []
        if system == 'Windows':
            import _winreg
            try:
                key = _winreg.OpenKey(
                    _winreg.HKEY_LOCAL_MACHINE, "HARDWARE\\DEVICEMAP\\SERIALCOMM")
                i = 0
                while True:
                    try:
                        values = _winreg.EnumValue(key, i)
                    except:
                        return baselist
                    if 'USBSER' in values[0] or \
                       'VCP' in values[0] or \
                       '\Device\Serial' in values[0]:
                        baselist.append(values[1])
                    i += 1
            except:
                return baselist
        else:
            for device in ['/dev/ttyACM*', '/dev/ttyUSB*', '/dev/tty.usb*', '/dev/tty.wchusb*',
                           '/dev/cu.*', '/dev/rfcomm*']:
                baselist = baselist + glob.glob(device)
        return baselist

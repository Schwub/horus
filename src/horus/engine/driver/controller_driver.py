# -*- coding: utf-8 -*-

import sys
import platform
import serial
import time

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ControllerNotConnected(Exception):

    def __init__(self):
        Exception.__init__(self, " Controller not conected")

class Controller(object):
    def __init__(self, serial_name='/dev/ttyUSB0', baud_rate=115200):
        self.serial_name=serial_name
        self.baud_rate=baud_rate
        self._serial_port = None
        self._connected = False

    @property
    def connected(self):
        return self._connected

    def connect(self):
        logger.info(" Connecting to controller {0} @baudrate {1}".format(self.serial_name, self.baud_rate))
        self._connected = False
        try:
            self._serial_port = serial.Serial(self.serial_name, self.baud_rate, timeout=2)
            #TODO: Check Firmware
            if self._serial_port.isOpen():
                logger.info(" Succesfully connected")
                self._connected = True
            else:
                raise ControllerNotConnected()
        except Exception as exception:
            logger.error(" Error opening the port {0}\n".format(self.serial_name))
            self._serial_port = None
            raise exception

    def send_command(self, command):
        time.sleep(2)
        #TODO: Check if finished
        self._serial_port.flushInput()
        self._serial_port.flushOutput()
        self._serial_port.write((command + "\r\n").encode())

__author__ = 'Michael Schwab'
__license__ = 'GNU General Public License v2 http://www.gnu.org/license/gpl2.html'

import logging

class Laser(object):
    def __init__(self, controller, pin):
        self._controller = controller
        self._pin = pin
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    def on(self):
        self._controller.send_command("M71T" + str(self._pin))
        self._is_on =True

    def off(self):
        self._controller.send_command("M70T" + str(self._pin))
        self._is_on = False


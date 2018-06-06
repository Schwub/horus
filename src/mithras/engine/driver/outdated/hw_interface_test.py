# -*- coding: utf-8 -*-
import hw_interface
import time

hw_interface = hw_interface.HW_Interface()
hw_interface.connect()
hw_interface.Laser_Left.on()
hw_interface.Laser_Right.on()
hw_interface.Laser_Left.off()
hw_interface.Laser_Right.off()
hw_interface.Table_Motor.acceleration = 200
hw_interface.Table_Motor.speed = 200
hw_interface.Table_Motor.move_right(100)
hw_interface.Table_Motor.move_left(100)
hw_interface.Table_Motor.move(200)
hw_interface.Table_Motor.invert_direction()
hw_interface.Table_Motor.move(200)
hw_interface.Table_Motor.move(300)
hw_interface.Table_Motor.move_to_position(0)

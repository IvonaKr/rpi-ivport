#!/usr/bin/env python
import rospy
import IIC


if __name__ == '__main__':
    rospy.init_node('init_ivport_node', anonymous = True)
    iviic = IIC.IIC(addr=(0x70), bus_enable =(0x01))
    print('proslo')

#!/usr/bin/env python

import baxter_interface
import rospy

if __name__ == '__main__':
    rospy.init_node("set_right_arm_py")
    names = ['right_e0', 'right_e1', 'right_s0', 'right_s1', 'right_w0', 'right_w1', 'right_w2']
    joints = [0.2515728492132078, 1.1443496677625187, 0.03681553890924993, -0.9836651802315216, -0.1054611791671222, 1.3698448435816746, -0.5744758050630875]
    combined = zip(names, joints)
    command = dict(combined)
    right = baxter_interface.Limb('right')
    right.move_to_joint_positions(command)
    print "Done"





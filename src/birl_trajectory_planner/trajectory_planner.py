#!/usr/bin/env python
import os
import rospy
import numpy as np
from dmp_util import dmp_generalization
from birl_trajectory_excution.utils import get_current_angle
from birl_inverse_kinematic import trac_ik_solver

dir_of_this_script = os.path.dirname(os.path.realpath(__file__))
demonstration_model_dir = os.path.join(dir_of_this_script, '..','..', 'dmp_data', 'processed_demonstrations','demos')


def planner(start=None, end=None,limb=None, planner_type = "dmp",phase=None, orig_demo_mode= None,point_mode=None):

    if planner_type == "cart_trajectory_action_server":
        joint = trac_ik_solver.inverse_kinematic(end,point_mode=point_mode,limb=limb)
        return joint
    elif planner_type == "dmp":
        joint_plan_list = dmp_plan(start,end,phase,limb=limb,orig_demo_mode=orig_demo_mode)
        return joint_plan_list

    elif planner_type == "promp":
        pass


def dmp_plan(start=None, end=None,limb=None,phase=None, orig_demo_mode= None):
    if phase == 1:
        rospy.loginfo("Dmp planner Phase: %s " %phase)
        demo = np.load(open(os.path.join(demonstration_model_dir,'home_to_prepick', '1.npy'), 'r'))
    elif phase == 2:
        rospy.loginfo("Dmp planner Phase: %s " %phase)
        demo = np.load(open(os.path.join(demonstration_model_dir,'prepick_to_pick', '1.npy'), 'r')) 
    elif phase == 3:
        rospy.loginfo("Dmp planner Phase: %s " %phase)
        demo = np.load(open(os.path.join(demonstration_model_dir,'prepick_to_pick', '1.npy'), 'r')) 
    elif phase == 4:
        rospy.loginfo("Dmp planner Phase: %s " %phase)
        demo = np.load(open(os.path.join(demonstration_model_dir, 'prepick_to_preplace','1.npy'), 'r')) 
    elif phase == 5:
        rospy.loginfo("Dmp planner Phase: %s " %phase)
        demo = np.load(open(os.path.join(demonstration_model_dir,'preplace_to_place','1.npy' ), 'r')) 
    elif phase == 6:
        rospy.loginfo("Dmp planner Phase: %s " %phase)
        demo = np.load(open(os.path.join(demonstration_model_dir, 'preplace_to_place','1.npy'), 'r')) 

    if orig_demo_mode != None:  
        start = demo[0]
        end  = demo[-1]
        rospy.loginfo("dmp orig start pose is %s\n" %start[0:3])
        rospy.loginfo("dmp orig end pose is %s\n" %end[0:3] )
    cart_trajectory_plan = dmp_generalization(start, end, demo)

    joint_plan_list = trac_ik_solver.inverse_kinematic(cart_trajectory_plan,limb=limb)

    return joint_plan_list
    
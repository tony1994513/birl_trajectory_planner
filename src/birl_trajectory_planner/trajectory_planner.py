#!/usr/bin/env python
import os
import rospy
import numpy as np
from birl_trajectory_excution import joint_action_client
from dmp_util import dmp_generalization
from birl_trajectory_excution.utils import get_current_angle
from birl_trajectory_excution._constant import limb
from birl_inverse_kinematic import trac_ik_solver

dir_of_this_script = os.path.dirname(os.path.realpath(__file__))
demonstration_model_dir = os.path.join(dir_of_this_script, '..','..', 'dmp_data', 'processed_demonstrations','demos')


def planner(start=None, end=None, planner_type = "dmp",phase=None, orig_demo_mode= None):

    if planner_type == "cart_trajectory_action_server":
        joint = trac_ik_solver.inverse_kinematic(end,one_point_mode=True)
        return joint
    elif planner_type == "dmp":
        joint_plan = dmp_plan(start,end,phase,orig_demo_mode)
        return joint_plan

    elif planner_type == "promp":
        pass


def dmp_plan(start=None, end=None,phase=None, orig_demo_mode= None):
    if phase == 1:
        rospy.loginfo("Dmp planner Phase: %s " %phase)
        demo = np.load(open(os.path.join(demonstration_model_dir,'home_to_prepick', '2.npy'), 'r'))
    elif phase == 2:
        rospy.loginfo("Dmp planner Phase: %s " %phase)
        demo = np.load(open(os.path.join(demonstration_model_dir,'prepick_to_pick', '2.npy'), 'r')) 
    elif phase == 3:
        rospy.loginfo("Dmp planner Phase: %s " %phase)
        demo = np.load(open(os.path.join(demonstration_model_dir,'prepick_to_pick', '2.npy'), 'r')) 
    elif phase == 4:
        rospy.loginfo("Dmp planner Phase: %s " %phase)
        demo = np.load(open(os.path.join(demonstration_model_dir, 'pre_pick_to_pre_place.npy'), 'r')) 
    elif phase == 5:
        rospy.loginfo("Dmp planner Phase: %s " %phase)
        demo = np.load(open(os.path.join(demonstration_model_dir, 'pre_place_to_place.npy'), 'r')) 
    elif phase == 6:
        rospy.loginfo("Dmp planner Phase: %s " %phase)
        demo = np.load(open(os.path.join(demonstration_model_dir, 'place_to_pre_place.npy'), 'r')) 

    if orig_demo_mode != None:  
        start = demo[0]
        end  = demo[-1]
    cart_trajectory_plan = dmp_generalization(start, end, demo)

    joint_plan = trac_ik_solver.inverse_kinematic(cart_trajectory_plan)

    return joint_plan
    
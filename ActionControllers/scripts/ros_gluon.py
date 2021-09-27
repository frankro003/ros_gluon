#! /usr/bin/env python3
import sys,time
import copy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

class RosGluon_bot(object):
    def __init__(self,_groupName):
        print('Connect MoveGroup...')
        self._groupName = _groupName
        moveit_commander.roscpp_initialize(sys.argv)
        self.move_group = moveit_commander.MoveGroupCommander('manipulator')
        self.robot = moveit_commander.RobotCommander()
    
    def get_PlanningFrame(self):
        time.sleep(5)
        return str(self.move_group.get_planning_frame())

    def get_EndffLink(self):
        return str(self.move_group.get_end_effector_link())
    
    def get_CurrentState(self):
        return self.robot.get_current_state()

    def get_GroupName(self):
        return str(self.robot.get_group_names())

    def get_CurrentJoint(self):
        return self.move_group.get_current_joint_values()

    def goal_Stop(self):
        self.move_group.stop()

    def goal_HomePose(self):
        _jointGoal = self.move_group.get_current_joint_values()
        _jointGoal[0] = pi/2
        _jointGoal[1] = 0.0
        _jointGoal[2] = -pi/2
        _jointGoal[3] = -pi/2
        _jointGoal[4] = -pi/2
        _jointGoal[5] = 0.0
        self.move_group.go(_jointGoal, wait=True)
        self.move_group.stop()

    def goal_ZeroAllPose(self):
        _jointGoal = self.move_group.get_current_joint_values()
        _jointGoal[0] = 0.0
        _jointGoal[1] = 0.0
        _jointGoal[2] = 0.0
        _jointGoal[3] = 0.0
        _jointGoal[4] = 0.0
        _jointGoal[5] = 0.0
        self.move_group.go(_jointGoal, wait=True)
        self.move_group.stop()

    def move_PlanningJointGoal_Rad(self,_joint):
        _jointGoal = self.move_group.get_current_joint_values()
        _jointGoal[0] = _joint[0]
        _jointGoal[1] = _joint[1]
        _jointGoal[2] = _joint[2]
        _jointGoal[3] = _joint[3]
        _jointGoal[4] = _joint[4]
        _jointGoal[5] = _joint[5]
        self.move_group.go(_jointGoal, wait=True)
        self.move_group.stop()

    def move_PlanningJointGoal_Deg(self,_joint):
        _jointGoal = self.move_group.get_current_joint_values()
        self._joint = _joint
        _jointGoal[0] = _joint[0] * pi/180
        _jointGoal[1] = _joint[1] * pi/180
        _jointGoal[2] = _joint[2] * pi/180
        _jointGoal[3] = _joint[3] * pi/180
        _jointGoal[4] = _joint[4] * pi/180
        _jointGoal[5] = _joint[5] * pi/180
        self.move_group.go(_jointGoal, wait=True)
        self.move_group.stop()

    def move_PlanningPoseGoal(self,_pose):
        if len(_pose) == 3:
            pose_goal = geometry_msgs.msg.Pose()
            pose_goal.orientation.w = 1
            pose_goal.position.x = _pose[0]
            pose_goal.position.y = _pose[1]
            pose_goal.position.z = _pose[2]
            self.move_group.set_pose_target(pose_goal)
            self.move_group.go(wait=True)
            self.move_group.stop()
            self.move_group.clear_pose_targets()
        else:
            ('Argument error (orint.w, pose.x, pose.y, pose.z)')
    



#! /usr/bin/env python

import rospy

import actionlib

from control_msgs.msg import (
    FollowJointTrajectoryAction,
    FollowJointTrajectoryFeedback,
    FollowJointTrajectoryResult,
)

from trajectory_msgs.msg import (
    JointTrajectoryPoint
)

class JointTrajectoryActionServer(object):

    def __init__(self, controller_name):
        self._action_ns = controller_name + '/follow_joint_trajectory'
        self._as = actionlib.SimpleActionServer(
                self._action_ns,
                FollowJointTrajectoryAction,
                execute_cb=self.execute_cb,
                auto_start = False)
        self._action_name = rospy.get_name()
        self._as.start()
        self._feedback = FollowJointTrajectoryFeedback
        self._result = FollowJointTrajectoryResult
        rospy.loginfo('Successful init')

    def execute_cb(self, goal):
        joint_names = goal.trajectory.joint_names
        trajectory_points = goal.trajectory.points
        rospy.loginfo(trajectory_points)

if __name__ == '__main__':
    rospy.init_node('gluon_interface')
    server = JointTrajectoryActionServer('arm_controller')
    rospy.spin()
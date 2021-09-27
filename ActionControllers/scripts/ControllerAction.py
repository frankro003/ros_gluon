#! /usr/bin/env python3
import innfos
import rospy
import time
from math import pi
import actionlib
from std_msgs.msg import String
from control_msgs.msg import FollowJointTrajectoryActionGoal

import jointstate_publisher
import TrajectoryGoal_subscriber

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
        print('\t- starting follow_joint_trajectory_action_server...')
        #self._actserver = actionlib.SimpleActionServer(controller_name+'/follow_joint_trajectory',
        #                                               FollowJointTrajectoryAction,self.execute_cb,False)
        #self._actserver.start()
        #rospy.loginfo('Successful init')
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
        self.actuID = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06]
        innfos.trapposmode(self.actuID)

    def execute_cb(self, goal):
        #joint_names = goal.trajectory.joint_names
        #trajectory_points = goal.trajectory.points

        _count = len(goal.trajectory.points)
        _msg = goal.trajectory.points
        _preTime = []
        _newTime = []


        for i in range(len(_msg)):
            _secP = str(_msg[i].time_from_start.secs) + '.' + str(_msg[i].time_from_start.nsecs)
            _preTime.append(float(_secP))

        for a in range(len(_msg)-1):
            print(_preTime[a])
            for b in range(len(_msg)-1):
                if _preTime[a] == _preTime[b]:
                    if _preTime[a] < _preTime[b+1]:
                        _newTime.append(_preTime[b])
                        break
                    elif _preTime[a] > _preTime[b+1]:
                        _newTime.append(_preTime[b+1])
                        _preTime[a+1] = _preTime[b]
                        _preTime[a] = _newTime[len(_newTime)-1]
                        break
        _newTime.append(_preTime[len(_preTime)-1])
        
        for i in range(_count):
            _speed = []
            r2rpm = 9.549297
            _speed.append(abs(_msg[i].velocities[0] * r2rpm)/56)
            _speed.append(abs(_msg[i].velocities[1] * r2rpm)/56)
            _speed.append(abs(_msg[i].velocities[2] * r2rpm)/56)
            _speed.append(abs(_msg[i].velocities[3] * r2rpm)/56)
            _speed.append(abs(_msg[i].velocities[4] * r2rpm)/56)
            _speed.append(abs(_msg[i].velocities[5] * r2rpm)/56)

            _access = [0,0,0,0,0,0]
            _decela = [0,0,0,0,0,0]
            if  abs(_msg[i].accelerations[0]) > 0:
                _access[0] = abs(_msg[i].accelerations[0])
                _decela[0] =  float('{:.3f}'.format(_access[0] * -1))
            else:
                _access[0] = 1.5
                _decela[0] = -1.5

            if  abs(_msg[i].accelerations[1]) > 0:
                _access[1] = abs(_msg[i].accelerations[1])
                _decela[1] = float('{:.3f}'.format(_access[1] * -1))
            else:
                _access[1] = 1.5
                _decela[1] = -1.5

            if  abs(_msg[i].accelerations[2]) > 0:
                _access[2] = abs(_msg[i].accelerations[2])
                _decela[2] = float('{:.3f}'.format(_access[2] * -1))
            else:
                _access[2] = 1.5
                _decela[2] = -1.5

            if  abs(_msg[i].accelerations[3]) > 0:
                _access[3] = abs(_msg[i].accelerations[3])
                _decela[3] = float('{:.3f}'.format(_access[3] * -1))
            else:
                _access[3] = 1.5
                _decela[3] = -1.5

            if  abs(_msg[i].accelerations[4]) > 0:
                _access[4] = abs(_msg[i].accelerations[4])
                _decela[4] = float('{:.3f}'.format(_access[4] * -1))
            else:
                _access[4] = 1.5
                _decela[4] = -1.5

            if  abs(_msg[i].accelerations[5]) > 0:
                _access[5] = abs(_msg[i].accelerations[5])
                _decela[5] =float('{:.3f}'.format(_access[5] * -1))
            else:
                _access[5] = 1.5
                _decela[5] = -1.5

            _pose = []
            _pose.append((_msg[i].positions[0] * 180/pi)/10)
            _pose.append((_msg[i].positions[1] * 180/pi)/10)
            _pose.append((_msg[i].positions[2] * 180/pi)/10)
            _pose.append((_msg[i].positions[3] * 180/pi)/10)
            _pose.append((_msg[i].positions[4] * 180/pi)/10)
            _pose.append((_msg[i].positions[5] * 180/pi)/10)



            delayTime = 0
            if i == 0:
                delayTime = 0
            else:
               # _secP = str(_msg[i].time_from_start.secs) + '.' + str(_msg[i].time_from_start.nsecs)
               # _secOld = str(_msg[i-1].time_from_start.secs) + '.' +  str(_msg[i-1].time_from_start.nsecs)
                delayTime = abs(_newTime[i] - _newTime[i-1])

            self.Acuator_Go(_speed,_access,_pose,_decela,delayTime)
#[1.5,1.5,1.5,1.5,1.5,1.5]
#[-.75,-.75,-.75,-.75,-.75,-.75]
    def Acuator_Go(self,speed,acc,_setpose,delelation,_delay):
        innfos.trapposset(self.actuID, acc, 
                        speed,
                        delelation)
        innfos.setpos(self.actuID, _setpose)
        time.sleep(_delay)

if __name__ == '__main__':
    rospy.init_node('gluon_interface')
    server = JointTrajectoryActionServer('gluon_bot')
    jointstate_publisher.robotJointState(rospy)
    TrajectoryGoal_subscriber.robotTrajectory(rospy)
    rospy.spin()
    
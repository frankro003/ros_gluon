#!/usr/bin/env python3
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import innfos
import time
from math import pi

class robotJointState:
    def __init__(self, _rospy):
        try:
            self._rospy = _rospy
            self.talker()
        except self._rospy.ROSInterruptException:
            pass

    def talker(self):
        #self._rospy.wait_for_service('/GluonServer/GetPose')
        
        pub = self._rospy.Publisher('joint_states', JointState, queue_size=10)
        #self.get_pose = self._rospy.ServiceProxy('/DobotServer/GetPose', Header)
        self.joint_msgs = JointState()
        rate = self._rospy.Rate(10)
        actuID = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06]
        #innfos.trapposmode(actuID)
        #time.sleep(3)
        while not self._rospy.is_shutdown():
            self.joint_msgs.header = Header()
            self.joint_msgs.header.stamp = self._rospy.Time.now()
            self.joint_msgs.name = ['axis_joint_1', 'axis_joint_2', 'axis_joint_3', 'axis_joint_4', 'axis_joint_5', 'axis_joint_6']
            self.joint_msgs.position = self.cvt2float(innfos.readpos(actuID),0)
            self.joint_msgs.velocity = self.cvt2float(innfos.readspd(actuID),1)
            self.joint_msgs.effort = [0,0,0,0,0,0]
            self._rospy.loginfo(self.joint_msgs)
            pub.publish(self.joint_msgs)
            rate.sleep()
    
    def cvt2float(self,_data,_unit):
        dataReturn=[0,0,0,0,0,0]
        if _unit == 0:
            for i in range(len(_data)):
                dataReturn[i] = (float(_data[i]) *10 ) * pi / 180
        elif _unit == 1:
            for i in range(len(_data)):
                dataReturn[i] = (float(_data[i])*0.017453)
        return dataReturn

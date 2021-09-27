#! /usr/bin/env python3
import time,ros_gluon
import threading
from functools import partial
from math import pi

myobject = ros_gluon.RosGluon_bot('manipulator')

try:
    import Tkinter as tk 
except ImportError:    
    import tkinter as tk 

def GoalHome():
    print('Goal_Home')
    threading.Thread(target=myobject.goal_HomePose).start()
    
def GoalZero():
    print('Goal_Zero')
    threading.Thread(target=myobject.goal_ZeroAllPose).start()
def SetJointGoal(_joint):
    print('Goal_Joint')
    _set=[]
    for i in range(len(_joint)):
        cvt = _joint[i].get()
        _set.append(float(cvt))
    print(_set)
    threading.Thread(target=myobject.move_PlanningJointGoal_Deg, args=(_set,)).start()

def SetPoseGoal(_pse):
    print('Goal_Pose')
    _set=[]
    for i in range(len(_pse)):
        cvt = _pse[i].get()
        _set.append(float(cvt))
    print(_set)
    threading.Thread(target=myobject.move_PlanningPoseGoal, args=(_set,)).start()

def _realtimeJointRead(_j1,_j2,_j3,_j4,_j5,_j6):
    while(True):
        #print(myobject.get_CurrentJoint())
        jointState = myobject.get_CurrentJoint()
        txtj1.set('J1: %.2f' %(jointState[0] *180/pi))
        txtj2.set('J2: %.2f' %(jointState[1]*180/pi))
        txtj3.set('J3: %.2f' %(jointState[2]*180/pi))
        txtj4.set('J4: %.2f' %(jointState[3]*180/pi))
        txtj5.set('J5: %.2f' %(jointState[4]*180/pi))
        txtj6.set('J6: %.2f' %(jointState[5]*180/pi))
        time.sleep(0.05)



root = tk.Tk()
root.geometry('550x160')
root.config(bg='#18191A')

root.title('GluonBot-Example Control GUI')

tk.Button(root,text='Goal-Home',bg='#e699ff',width=10,command=GoalHome).place(x=5,y=5)
tk.Button(root,text='Goal-Zero',bg='#e699ff',width=10,command=GoalZero).place(x=5,y=35)

txtj1 = tk.StringVar(root)
txtj2 = tk.StringVar(root)
txtj3 = tk.StringVar(root)
txtj4 = tk.StringVar(root)
txtj5 = tk.StringVar(root)
txtj6 = tk.StringVar(root)

j1_lable = tk.Label(root,textvariable =txtj1,bg='#18191A',text='J1: 0.0',fg='#ECF0F1',font=('Times', 12)).place(x=150,y=7)
j2_lable = tk.Label(root,textvariable =txtj2,bg='#18191A',text='J2: 0.0',fg='#ECF0F1',font=('Times', 12)).place(x=270,y=7)
j3_lable = tk.Label(root,textvariable =txtj3,bg='#18191A',text='J3: 0.0',fg='#ECF0F1',font=('Times', 12)).place(x=400,y=7)
j4_lable = tk.Label(root,textvariable =txtj4,bg='#18191A',text='J4: 0.0',fg='#ECF0F1',font=('Times', 12)).place(x=150,y=37)
j5_lable = tk.Label(root,textvariable =txtj5,bg='#18191A',text='J5: 0.0',fg='#ECF0F1',font=('Times', 12)).place(x=270,y=37)
j6_lable = tk.Label(root,textvariable =txtj6,bg='#18191A',text='J6: 0.0',fg='#ECF0F1',font=('Times', 12)).place(x=400,y=37)

j1Get = tk.StringVar(root,value='0.0')
j2Get = tk.StringVar(root,value='0.0')
j3Get = tk.StringVar(root,value='0.0')
j4Get = tk.StringVar(root,value='0.0')
j5Get = tk.StringVar(root,value='0.0')
j6Get = tk.StringVar(root,value='0.0')

tk.Entry(root,width=8, textvariable=j1Get).place(x=150,y=70)
tk.Entry(root, width=8,textvariable=j2Get).place(x=150,y=95)
tk.Entry(root, width=8,textvariable=j3Get).place(x=150,y=120)
tk.Entry(root,width=8, textvariable=j4Get).place(x=220,y=70)
tk.Entry(root, width=8,textvariable=j5Get).place(x=220,y=95)
tk.Entry(root, width=8,textvariable=j6Get).place(x=220,y=120)
_floatJ = [j1Get,j2Get,j3Get,j4Get,j5Get,j6Get]

SetJointGoal = partial(SetJointGoal, _floatJ)
tk.Button(root,text='Goal-Joint',bg='#99ccff',width=10,height=4,command=SetJointGoal).place(x=5,y=70)


poseX = tk.StringVar(root,value='0.0')
poseY = tk.StringVar(root,value='0.0')
poseZ = tk.StringVar(root,value='0.0')
tk.Entry(root,width=8, textvariable=poseX).place(x=450,y=70)
tk.Entry(root, width=8,textvariable=poseY).place(x=450,y=95)
tk.Entry(root, width=8,textvariable=poseZ).place(x=450,y=120)
_floatP = [poseX,poseY,poseZ]
SetPoseGoal = partial(SetPoseGoal, _floatP)
tk.Button(root,text='Goal-Pose',bg='#99ff99',width=10,height=4,command=SetPoseGoal).place(x=320,y=70)

x = threading.Thread(target=_realtimeJointRead,args=(j1_lable,j2_lable,j3_lable,j4_lable,j5_lable,j6_lable))
x.start()


root.mainloop() 

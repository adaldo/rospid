#! /usr/bin/env python

import rospy as rp
import geometry_msgs.msg as gms

import abstract as abt




class Zero(abt.Abstract):


    def control_law(self, time):
        #raise NotImplementedError()
        return gms.Vector3()



if __name__ == '__main__':
    rp.init_node('zero')
    controller = Zero()
    controller.start()

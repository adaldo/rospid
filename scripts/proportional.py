#! /usr/bin/env python

import rospy as rp
import geometry_msgs.msg as gms
import abstract as abt

import dynamic_reconfigure.server as drs
import rospid.cfg.ProportionalConfig as pc
#import dynamic_tutorials.cfg as dtc

import numpy as np
import copy as cp



class Proportional(abt.Abstract):

    def reconfig_callback(self, config, level):
        self.LOCK.acquire()
        #rp.logwarn(self.__GAIN)
        self.__GAIN[0][0] = config["x"]
        #self.__GAIN[0][1] = config["xy"]
        #self.__GAIN[1][0] = config["xy"]
        #self.__GAIN[0][2] = config["xz"]
        #self.__GAIN[2][0] = config["xz"]
        self.__GAIN[1][1] = config["y"]
        #self.__GAIN[1][2] = config["yz"]
        #self.__GAIN[2][1] = config["yz"]
        self.__GAIN[2][2] = config["z"]
        #rp.logwarn(self.__GAIN)
        self.LOCK.release()
        return config

    def control_law(self, time):
        pt = np.array([self.point.x, self.point.y, self.point.z])
        ref = np.array([self.reference.x, self.reference.y, self.reference.z])
        control = self.__GAIN.dot(ref-pt)
        return gms.Vector3(*(control.tolist()))


    @property
    def GAIN(self):
        return self.__GAIN


    def __init__(self,
            frequency=rp.get_param('frequency', 1e1),
            gain=np.array(rp.get_param('gain', np.eye(3).tolist()))):
            #gain = rp.get_param('gain', 1.0)):
        abt.Abstract.__init__(self, frequency)
        self.__GAIN = gain
        drs.Server(pc, self.reconfig_callback)


if __name__ == '__main__':
    rp.init_node('proportional')
    controller = Proportional()
    controller.start()

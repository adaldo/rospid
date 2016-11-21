#! /usr/bin/env python

import rospy as rp
import geometry_msgs.msg as gms

import threading as thd
import copy as cp

class Abstract:


    def __compute_control(self, time):
        self.LOCK.acquire()
        control = self.control_law(time)
        self.LOCK.release()
        return control

    def control_law(self, time):
        raise NotImplementedError()
        #return gms.Vector3()

    def point_callback(self, msg):
        self.LOCK.acquire()
        self.__point = msg
        self.LOCK.release()

    def reference_callback(self, msg):
        self.LOCK.acquire()
        self.__reference = msg
        self.LOCK.release()


    @property
    def point(self):
        return cp.copy(self.__point)

    @property
    def reference(self):
        return cp.copy(self.__reference)



    def __init__(self,
            frequency=rp.get_param('frequency', 1e1)):
        self.__point = None
        self.__reference = None
        self.LOCK = thd.Lock()
        self.__pub = rp.Publisher(
            name='control',
            data_class=gms.Vector3,
            queue_size=10)
        rp.Subscriber(
            name='point',
            data_class=gms.Point,
            callback=self.point_callback)
        rp.Subscriber(
            name='reference',
            data_class=gms.Point,
            callback=self.reference_callback)
        self.__INITIAL_TIME = rp.get_time()
        self.__RATE = rp.Rate(frequency)
        self.__first_received_flag = False


    def start(self):
        while not rp.is_shutdown() and not self.__first_received_flag:
            self.LOCK.acquire()
            point = cp.copy(self.__point)
            reference = cp.copy(self.__reference)
            self.LOCK.release()
            if not point is None and not reference is None:
                self.__first_received_flag = True
            self.__RATE.sleep()
        while not rp.is_shutdown():
            time = rp.get_time()-self.__INITIAL_TIME
            self.LOCK.acquire()
            point = cp.copy(self.__point)
            reference = cp.copy(self.__reference)
            self.LOCK.release()
            control = self.__compute_control(time)
            self.__pub.publish(control)
            self.__RATE.sleep()



if __name__ == '__main__':
    rp.init_node('abstract')
    controller = Abstract()
    controller.start()

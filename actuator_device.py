from device import device
import copy as copy
import random
import threading

DEVBOT_TIMER = 2



class actuator_device(device):
    def __init__(self, config):
        super().__init__()
        self.device_profile["ACTDEV"]=dict()
        self.device_profile["ACTDEV"]["ATTR"]=copy.deepcopy(config)
        stat=list()
        for dev in config:
            one=dict()
            one['DeviceID']=dev['DeviceID']
            one['OperationStatus']='OFF'
            one['OperationDuration']=0
            one['OperationTime']=0
            one['OperationSpeed']=0
            one['OperationPosition']=0
            stat.append(one)
        self.device_profile["ACTDEV"]["STATUS"]=stat

        # self.run_devbot(DEVBOT_TIMER)

      

    def devbot(self):
        self.run_devbot(DEVBOT_TIMER)
        
    def run_devbot(self, period):
        self.bottimer = threading.Timer(period, self.devbot)
        self.bottimer.start()



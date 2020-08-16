from device import device
import copy as copy
import random
import threading
import sensor_temphumid

DEVBOT_TIMER = 2

class sensor_device(device):
    def __init__(self, config):
        super().__init__()
        self.device_profile["SENSDEV"]=dict()
        self.device_profile["SENSDEV"]["ATTR"]=copy.deepcopy(config)
        stat=list()
        for dev in config:
            one=dict()
            one['DeviceID']=dev['DeviceID']
            one['DeviceType']=dev['DeviceType']
            one['SensingValue']=None
            one['ValueType']=None
            one['valuerange']=dev['valuerange']
            
            stat.append(one)
        self.device_profile["SENSDEV"]["STATUS"]=stat
        
        self.run_devbot(DEVBOT_TIMER)

    def devbot(self):
        temperature, humidity = sensor_temphumid.get_sensor_value()
        if(temperature is not None and humidity is not None):
            for device in self.device_profile["SENSDEV"]["STATUS"]:
                if(device['DeviceType']=='temperature'):    device['SensingValue']=temperature
                elif(device['DeviceType']=='humidity'):     device['SensingValue']=humidity
                else: device["SensingValue"]= round(random.uniform(device["valuerange"]["min"],device["valuerange"]["max"]),2)

            
        self.run_devbot(DEVBOT_TIMER)
        
    def run_devbot(self, period):
        
        self.bottimer = threading.Timer(period, self.devbot)
        self.bottimer.start()



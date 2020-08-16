
from node import node
from actuator_device import actuator_device
from scp import scp
from lcp import lcp

import yaml, json
import lcp_def as lcpdef
import sys
from time import sleep
from colorama import Fore
from colorama import Style
import argparse

STATE_IDLE = 0
STATE_REGISTERING = 1
STATE_REGISTERED = 2

class actuator_node(node):
    def __init__(self, config):

        self.config = config 

        node.__init__(self, self.config["NODE"])
        self.device = actuator_device(self.config["ACTDEV"])
        self.state      = STATE_IDLE        

    def startup(self, port):
        if(port is None):       self.run(self.config["NODE"]["port"])
        else:                   self.run(port)

        sleep(0.1)      # sleep을 안 넣어주면, register가 먼저 수행됨에 따라 socket bind error가 발생될 수 있다.

        self.scp_request_nodereg(payload=self.config)
        self.state      = 1 # STATE_REGISTERING

    def onrecvGETreq(self, lcp_message, address):
        device_status = self.device.device_getstatus(lcp_message["payload"])
        if(device_status is None):  self.scp_send_actdevstat(rsp_code=404, req_msg=lcp_message, payload=None)
        else:                       self.scp_send_actdevstat(rsp_code=200, req_msg=lcp_message, payload=device_status)   

        return

    def onrecvPUTreq(self, lcp_message, address):

        if(lcp_message["payload"] is not None):
            payload=json.loads(lcp_message["payload"])
            cmd = payload.get('ActDevControl')
            if(cmd is not None): 
                device_status = self.device.device_setstatus(cmd=cmd)
                if(device_status is None):  self.scp_respond(rsp_code=404, req_msg=lcp_message, payload=None)
                else:                       self.scp_send_actdevstat(rsp_code=200, req_msg=lcp_message, payload=device_status) 
        

    def onrecvPOSTreq(self, lcp_message, address):
        self.scp_respond(rsp_code=500, req_msg=lcp_message, payload=None)
        return    


    def onrecv2xxrsp(self, lcp_message, address):
        if(self.state == STATE_REGISTERING): self.state = STATE_REGISTERED      
        return    
           
  

#######################################################
# MAIN
#######################################################

def print_menu():
    print("---- Choose ----")
    print("[1] send register message")
    print("[2] query device 'ACTDEV/STATUS/DeviceID:1'")
    print("[3] send 'ACTDEV/STATUS/DeviceID:1' with POST")
    print("[0] exit ")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--nodeid', type=int,
                help="node local id")
    parser.add_argument('-p', '--port', type=int,
                help="port")

    args = parser.parse_args()

    fd = open("./actuator_node_cfg.yaml",'r')
    config = yaml.load(fd)  

    if(args.nodeid is not None):    config["NODE"]["id"] = args.nodeid
    if(args.port is not None):      config["NODE"]["port"] = args.port

    actuator_node = actuator_node(config)
    actuator_node.startup(None)
    

    for line in sys.stdin:
        line = line.split()
        if(len(line) >0):
            if(line[0]=='1'):   actuator_node.scp_request_nodereg(payload=actuator_node.config)
            elif(line[0]=='2'): print(actuator_node.device.device_getstatus('ACTDEV/STATUS/DeviceID:1'))
            elif(line[0]=='3'): actuator_node.scp_send_actdevstat(None, None, payload=actuator_node.device.device_getstatus('ACTDEV/STATUS/DeviceID:1'))
            elif(line[0]=='0'): sys.exit(1)
        print_menu()

    


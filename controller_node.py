
from node import node
from device import device
from scp import scp
from lcp import lcp
import scp as scpdef

import yaml, json
import lcp_def as lcpdef
import sys
from time import sleep


class controller_node(node):
    
    nodedict=dict()
    # nodelist=list()
    house_env_policy=dict()     # 온도, 습도, 이산화탄소, 조도(광량)
    def __init__(self, config):
        
        self.config = config  

        node.__init__(self, self.config["NODE"])

    def startup(self, port):
        if(port is None):       self.run(self.config["NODE"]["port"])
        else:                   self.run(port)

        sleep(0.1)      # sleep을 안 넣어주면, register가 먼저 수행됨에 따라 socket bind error가 발생될 수 있다.

        self.scp_request_nodereg(payload=self.config)

    def CONTROLLER_request_devstat(self, targetid):
        target = targetid.split('@')
        print(target)
        if(targetid.find('SENS') is not None):  
            if(len(target)==2):
                self.scp_request_sensdevstat(dst_id=int(target[0]), target=target[1])
            else:
                for k, v in self.nodedict.items():
                    if(v['NODE']['type']==0): self.scp_request_sensdevstat(dst_id=k, target=target[0])
        if(targetid.find('ACT') is not None):  
            if(len(target)==2):
                self.scp_request_actdevstat(dst_id=int(target[0]), target=target[1])
            else:
                for k, v in self.nodedict.items():
                    if(v['NODE']['type']==1): self.scp_request_actdevstat(dst_id=k, target=target[0])
   
        
    def onrecvREGreq(self, lcp_message, address):
        NodeRegMsg=json.loads(lcp_message["payload"])
        self.nodedict[lcp_message["source_id"]]=NodeRegMsg["NodeReg"]
        self.scp_respond(rsp_code=200, req_msg=lcp_message, payload=None)   
        self.scp_forward(payload=lcp_message["payload"])
        return      

    def onrecvGETreq(self, lcp_message, address):
        #   - 1. GOS로부터 GET을 받으면, 202 Accepted를 보내고
        #   - 2. 해당 노드에게 GET을 보냄. (TODO)
        #   - 3. 해당 노드로부터 200을 받으면, POST로 GOS에게 결과를 송신함.
        self.scp_respond(rsp_code=202, req_msg=lcp_message, payload=None) 
        self.CONTROLLER_request_devstat(lcp_message['payload'])

        return 

    def onrecvPOSTreq(self, lcp_message, address):
        self.scp_respond(rsp_code=200, req_msg=lcp_message, payload=None)
        self.scp_forward(payload=lcp_message["payload"])
        return    


    def onrecv2xxrsp(self, lcp_message, address):
        self.scp_forward(payload=lcp_message["payload"])
        return



#######################################################
# MAIN
#######################################################

def print_menu():
    print("---- Choose ----")
    print("[1] Register SGc to SGos")
    print("[2] List registered nodes ")
    print("[3] TEST - request all sensor node status 'SENSDEV' ")
    print("[4] TEST - request all device node 'ON' ")
    print("[4] TEST - request all device node 'OFF' ")
    print("[0] exit ")



if __name__ == "__main__":


    fd = open("./controller_node_cfg.yaml",'r')
    config = yaml.load(fd)  

    controller_node = controller_node(config)
    controller_node.startup(None)

    for line in sys.stdin:
        line = line.split()
        if(len(line) >0):
            if(line[0]=='1'):    
                controller_node.scp_request_nodereg(payload=controller_node.config)
                # nodelist=list()
                # for key, value in controller_node.nodedict.items():
                #     nodelist.append(value)   
                # controller_node.scp_request_nodereg(payload=nodelist)
            elif(line[0]=='2'):       print(controller_node.nodedict)
            elif(line[0]=='3'):     
                for k, v in controller_node.nodedict.items():
                    if(v['NODE']['type']==0): controller_node.scp_request_sensdevstat(dst_id=k, target="SENSDEV/STATUS")
                    elif(v['NODE']['type']==1): controller_node.scp_request_actdevstat(dst_id=k, target="ACTDEV/STATUS")
            elif(line[0]=='4'):    
                for k, v in controller_node.nodedict.items():
                    if(v['NODE']['type']==1): controller_node.scp_request_actdevctrl(dst_id=k, control=scpdef.SCP_CONTROL_ACTDEV_ON, target="ACTDEV/STATUS")
            elif(line[0]=='5'):    
                for k, v in controller_node.nodedict.items():
                    if(v['NODE']['type']==1): controller_node.scp_request_actdevctrl(dst_id=k, control=scpdef.SCP_CONTROL_ACTDEV_OFF, target="ACTDEV/STATUS")                                         
            elif(line[0]=='0'): sys.exit(1)
        else:
            pass
        print_menu()

    
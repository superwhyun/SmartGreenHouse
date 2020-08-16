
from node import node
from device import device
from scp import scp
from lcp import lcp
import sgmongo
import sgrest


import yaml, json
import lcp_def as lcpdef
import sys
from time import sleep
from datetime import datetime


class operator_node(node):
    mongoif = sgmongo.SGmongo()
    nodes=dict()
    def __init__(self, config):
        
        self.config = config  

        node.__init__(self, self.config["NODE"])

    def startup(self, port):
        if(port is None):       self.run(self.config["NODE"]["port"])
        else:                   self.run(port)
           

    def onrecvREGreq(self, lcp_message, address):
        self.nodes[lcp_message["source_id"]]=json.loads(lcp_message["payload"])
        self.scp_respond(rsp_code=200, req_msg=lcp_message, payload=None)        
        
        if(lcp_message["payload"] is not None):
            payload=json.loads(lcp_message["payload"])
            for k, v in payload.items():
                if(k == 'NodeReg'):
                    v['NODE']['nodeid']=lcp_message["source_id"]
                    self.mongoif.saveControllerNodeInfo(node_info=v)

        return      

    def onrecvPOSTreq(self, lcp_message, address):

        self.scp_respond(rsp_code=200, req_msg=lcp_message, payload=None)   

        if(lcp_message["payload"] is not None):
            payload=json.loads(lcp_message["payload"])
            nodeid=payload.get('NodeID')
            reginfo=payload.get('NodeReg')
            sensinfo=payload.get('SensDevStat')
            actinfo=payload.get('ActDevStat')

            if(reginfo is not None):
                reginfo['cnode_id']=lcp_message["source_id"]
                self.mongoif.saveDevNodeInfo(node_info=reginfo)

            if(sensinfo is not None):
                for item in sensinfo:
                    item['NodeID']=nodeid
                    item['timestamp']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.mongoif.saveDevStatusInfo(status=sensinfo)
            
            if(actinfo is not None):
                for item in actinfo:
                    item['NodeID']=nodeid
                    item['timestamp']=datetime.utcnow()
                self.mongoif.saveDevStatusInfo(status=actinfo)

        return    


#######################################################
# MAIN
#######################################################

def print_menu():
    print("---- Choose ----")
    print("[1] list house/controller node ")
    print("[2] list all sensor node status 'SENSDEV' ")
    print("[3] list sensor node status '129@SENSDEV/STATUS/DeviceID:1' ")
    print("[0] exit ")



if __name__ == "__main__":


    fd = open("./operator_node_cfg.yaml",'r')
    config = yaml.load(fd)  

    operator_node = operator_node(config)
    operator_node.startup(None)

    restful = sgrest.myFLASK(__name__)
    restful.run()

    for line in sys.stdin:
        line = line.split()
        if(len(line) >0):
            if(line[0]=='1'):       print(operator_node.nodes)
            elif(line[0]=='2'):     
                for k, v in operator_node.nodes.items():
                    operator_node.scp_request_sensdevstat(dst_id=k, target="SENSDEV/STATUS")
            elif(line[0]=='3'):     
                for k, v in operator_node.nodes.items():
                    # operator_node.scp_request_sensdevstat(dst_id=k, target={'Target-Node': 49281, 'Target': "SENSDEV/STATUS:id=1"})
                    operator_node.scp_request_sensdevstat(dst_id=k, target="129@SENSDEV/STATUS/DeviceID:1")
            elif(line[0]=='0'): sys.exit(1)
        else:
            pass
        print_menu()

    
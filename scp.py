import struct
import random
from lcp import lcp
import lcp_def as sfdef
import json

SCP_CONTROL_ACTDEV_OPEN = 2000
SCP_CONTROL_ACTDEV_CLOSE = 2001
SCP_CONTROL_ACTDEV_ON = 2002
SCP_CONTROL_ACTDEV_OFF = 2003


class scp(lcp):
    def __init__(self, nid, rootid):
        self.nid = nid
        self.rootid = rootid
        super().__init__()
        pass


    def scp_request_nodereg(self, payload):
        # self.lcp_register(nid, rootid, json.dumps(payload, indent=2))
        myload=dict()
        myload['NodeReg']=payload
        self.lcp_register(self.nid, self.rootid, payload=json.dumps(myload))
        
        pass

    def scp_request_actdevstat(self, dst_id, target):
        self.lcp_get(
            src=self.nid, 
            dst=dst_id, 
            payload=target)
        return

    def scp_request_sensdevstat(self, dst_id, target):
        self.lcp_get(
            src=self.nid, 
            dst=dst_id, 
            payload=target)
        return

    def scp_request_actdevctrl(self, dst_id, control, target):
        myload=dict()
        command=dict()
        command['TargetID']=target
        if(control == SCP_CONTROL_ACTDEV_ON):
            command['OperationCommand']='ON'
            command['OperationDuration']=0
            command['OperationTime']='01:00:00'
            command['OperationSpeed']=1
            command['FeedbackRequest']=False
        elif(control == SCP_CONTROL_ACTDEV_OFF):
            command['OperationCommand']='OFF'
            command['OperationDuration']=0
            command['OperationTime']='00:00:00'
            command['OperationSpeed']=0
            command['FeedbackRequest']=False            

        myload['ActDevControl']=command
        self.lcp_put(
            src=self.nid, 
            dst=dst_id, 
            payload=json.dumps(myload))
        return


    def scp_send_actdevstat(self, rsp_code, req_msg, payload):
        
        if(payload is not None): 
            # myload=dict()
            # payload['NodeID']=self.nid
            # myload['ActDevStat']=payload
            myload={'NodeID': self.nid, 'ActDevStat' : payload }
            actdevstat = json.dumps(myload)
        else:
            actdevstat = None

        if(rsp_code == None or req_msg == None):
            self.lcp_post(
                src=self.nid,
                dst=self.rootid,
                payload=actdevstat
            )
        else:
            self.lcp_respond(
                src=self.nid,
                dst=self.rootid,
                rspcode=rsp_code,
                msgid=req_msg["message_id"], 
                payload=actdevstat
            )
        
        return



    def scp_send_sensdevstat(self, rsp_code, req_msg, payload):
        
        devstat=list()

        if(payload is not None):
            for item in payload:
                one=dict()
                for k, v in item.items():
                    if(v is not None and ( k == 'DeviceID' or k == 'SensingValue' )):
                        one[k]=v
                    # if(v is not None and k != 'valuerange'):
                    #     one[k]=v
                if( one.get('SensingValue') is not None):
                    devstat.append(one)

        myload={'NodeID': self.nid, 'SensDevStat' : devstat }
        if(rsp_code == None or req_msg == None):
            self.lcp_post(
                src=self.nid,
                dst=self.rootid,
                payload=json.dumps(myload)
            )
        else:
            self.lcp_respond(
                src=self.nid,
                dst=self.rootid,
                rspcode=rsp_code,
                msgid=req_msg["message_id"], 
                payload=json.dumps(myload)
            )
        
        return


    #
    # child node로부터 받은 POST메시지의 payload를 신규 POST를 이용하여 root node로 전송한다.
    #
    def scp_forward(self, payload):
        self.lcp_post(
            src=self.nid,
            dst=self.rootid,
            payload=payload
        )

        return

    def scp_respond(self, rsp_code, req_msg, payload):
        self.lcp_respond(
            src=req_msg["dest_id"],
            dst=req_msg["source_id"], 
            rspcode=rsp_code, 
            msgid=req_msg["message_id"], 
            payload=payload)
        return







    def onrecv(self, message, address):
        
        lcp_message = self.node.parseMessage(message)
        if   (lcp_message["T"] == 0): self.onrecv_req(message, address)
        elif (lcp_message["T"] == 2): self.onrecv_rsp(message, address)

    def onrecv_request(self, message, address):

        pass

    def onrecv_response(self, message, address):

        pass    
        


if __name__ == "__main__":

    ipa=scp()
    ipa.listen(5000)    
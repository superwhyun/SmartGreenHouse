
from scp import scp
import lcp_def as lcpdef


class node(scp):

    def __init__(self, config):
        
        self.nodetype   = config["type"]
        self.houseid    = config["houseid"]
        self.nodeid     = (self.nodetype << 14) ^ (self.houseid << (14-config["masklen"])) ^ (config["id"])
        config["nodeid"]=self.nodeid

        if(self.nodetype != 2):
            self.rootid     = (config["root"]["type"] << 14) ^ (self.houseid << (14-config["masklen"])) ^ (config["root"]["id"])
        else:
            self.rootid     = 0

        super().__init__(self.nodeid, self.rootid)

        if(self.nodetype !=2):
            self.netif_addressmap_add(self.rootid, config["root"]["address"], config["root"]["port"])

    def onrecv(self, message, address):
        lcp_message = self.lcp_parse_message(message)

        if   (lcp_message["T"]  == 0):   self.onrecv_req(lcp_message, address)
        elif (lcp_message["T"]  == 2):   self.onrecv_rsp(lcp_message, address)


    ##############################################################
    # Virtual functions to be overrided/implemented child class
    ##############################################################
    def onrecvGETreq(self, lcp_message, address):
        self.scp_respond(rsp_code=500, req_msg=lcp_message, payload=None)
        return
    def onrecvPOSTreq(self, lcp_message, address):
        self.scp_respond(rsp_code=500, req_msg=lcp_message, payload=None)
        return
    def onrecvPUTreq(self, lcp_message, address):
        self.scp_respond(rsp_code=500, req_msg=lcp_message, payload=None)
        return
    def onrecvREGreq(self, lcp_message, address):
        self.scp_respond(rsp_code=500, req_msg=lcp_message, payload=None)
        return        

    def onrecv1xxrsp(self, lcp_message, address):
        pass
    def onrecv2xxrsp(self, lcp_message, address):
        pass
    def onrecv3xxrsp(self, lcp_message, address):
        pass
    def onrecv4xxrsp(self, lcp_message, address):
        pass
    def onrecv5xxrsp(self, lcp_message, address):
        pass
    def onrecv6xxrsp(self, lcp_message, address):
        pass                    

    def onrecv_req(self, lcp_message, address):
        self.PrintEventLog(self.EVENT_INFO, "[REQ RECEIVED]")
        self.lcp_print_message(lcp_message)

        if(lcp_message["code_low"]==lcpdef.METHOD_GET): return self.onrecvGETreq(lcp_message, address)
        elif(lcp_message["code_low"]==lcpdef.METHOD_PUT): return self.onrecvPUTreq(lcp_message, address)
        elif(lcp_message["code_low"]==lcpdef.METHOD_POST): return self.onrecvPOSTreq(lcp_message, address)
        elif(lcp_message["code_low"]==lcpdef.METHOD_REG): return self.onrecvREGreq(lcp_message, address)
        


    # Root node로부터 받은 응답은 내부적 처리(재전송 타이머 리셋 등)만 처리하고 위로 올려보내지 않는다.
    def onrecv_rsp(self, lcp_message, address):
        self.PrintEventLog(self.EVENT_INFO, "[RSP RECEIVED]")
        self.lcp_print_message(lcp_message)

        if(lcp_message["source_id"] == self.rootid): return

        if(lcp_message["code_high"]==1): return self.onrecv1xxrsp(lcp_message, address)
        elif(lcp_message["code_high"]==2): return self.onrecv2xxrsp(lcp_message, address)
        elif(lcp_message["code_high"]==3): return self.onrecv3xxrsp(lcp_message, address)
        elif(lcp_message["code_high"]==4): return self.onrecv4xxrsp(lcp_message, address)
        elif(lcp_message["code_high"]==5): return self.onrecv5xxrsp(lcp_message, address)
        elif(lcp_message["code_high"]==6): return self.onrecv6xxrsp(lcp_message, address)



if __name__ == "__main__":
    
    ipa=node()
    ipa.listen(5000)
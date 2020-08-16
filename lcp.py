
import struct
import random

from ipadaptor import IpAdaptor
from copy import deepcopy
import lcp_def as sfdef


def p8(x): return struct.pack('>B', x)
def p16(x): return struct.pack('>H', x)
def p32(x): return struct.pack('>I', x)
def pStr(x):
    fmt = '>' + len(x) + 's'
    return struct.pack(fmt, x)

def u8(x): return struct.unpack('>B', x)[0]
def u16(x): return struct.unpack('>H', x)[0]
def u32(x): return struct.unpack('>I', x)[0]

def p_sf(oct, code, mid, src, dst, len): 
    return struct.pack('>BBHHHH', oct, code, mid, src, dst, len)

def u_sf(x):
    return struct.unpack('>BBHHHH', x)





lcp_msg_template ={
    ### first
    "V" : 1,
    "T" : 0,             # 요청(0) , 알림(1), 응답(2), 리셋(3)
    "P" : 0,     # none(0), binary(2), text(3)
    "R" : 0,

    ### second
    "code_high" : 0,        # 요청(0), 응답-성공(2), 응답-실패(4)
    "code_low" : 0,         # 요청일 경우, GET(1), POST(2), PUT(3), REG(5), REL(6), HB(7)

                            # Code	의미
                            # 0.01	 GET
                            # 0.02	 POST
                            # 0.03	 PUT
                            # 0.05	 Registration
                            # 0.06	 Release
                            # 0.07	 Heartbeat

                            # 2.00	 OK
                            # 2.04	 Changed                               
                            # 2.05	 Content                               

                            # 4.00	 Bad Request                           
                            # 4.01	 Unauthorized                           
                            # 4.03	 Forbidden                             
                            # 4.04	 Not Found                             
                            # 4.05	 Method Not Allowed                   
                            # 4.06	 Not Acceptable                        
                            # 4.15	 Unsupported Content-Format            

    ### third
    "message_id" : 0,       # random generation

    ### fourth
    "source_id" : 0,        # 2byte
    "dest_id"   : 0,        # 2byte

    ### fifth
    "payload_length" : 0,   # 2byte
    "payload" : ""        # variable; 0~65535 bytes
}



class lcp(IpAdaptor):
    def __init__(self):
        super().__init__()
        
        self.message_id = random.randint(0, 2000)
        pass

    def lcp_print_message(self, msg):
        if(msg["code_high"] == 0): 
            if(msg["code_low"]==sfdef.METHOD_GET): method="GET "
            elif(msg["code_low"]==sfdef.METHOD_POST): method="POST"
            elif(msg["code_low"]==sfdef.METHOD_PUT): method="PUT "
            elif(msg["code_low"]==sfdef.METHOD_REG): method="REG "
            elif(msg["code_low"]==sfdef.METHOD_REL): method="REL "
            elif(msg["code_low"]==sfdef.METHOD_HB): method="HB  "
            else: method="Unknown"
        else:
            method=str(msg["code_low"])+"   "

        print("+-----+-----+-----+-----+------------------+-----------------------------------------+")
        print("| V=%d | T=%d | P=%d | R=%d |  HC=%d / LC=%s  |             MessageID=%4d              |" % 
                (msg["V"],msg["T"],msg["P"],msg["R"],msg["code_high"], method, msg["message_id"]))
        print("+------------------------------------------+-----------------------------------------+")        
        print("|              Source ID=%d             |             Dest ID=%d               |" % 
                (msg["source_id"], msg["dest_id"]))
        print("+------------------------------------------+-----------------------------------------+")             
        print("|              Length=%4d                 |              Payload = " % (msg["payload_length"]))
        print("+------------------------------------------+")             
        
        print(" %s" % (msg.get("payload")))
        print("+------------------------------------------------------------------------------------+")             


    def lcp_parse_message(self, message):
        
        tupled = u_sf(message[:10])
        parsed = dict()
        parsed["V"] = (tupled[0] >> 6) & 3
        parsed["T"] = (tupled[0] >> 4) & 3
        parsed["P"] = (tupled[0] >> 2) & 3
        parsed["R"] = (tupled[0]) & 3
        parsed["code_high"] = (tupled[1] >> 4)
        parsed["code_low"] = (tupled[1] & 15)
        parsed["message_id"] = tupled[2]
        parsed["source_id"] = tupled[3]
        parsed["dest_id"] = tupled[4]
        parsed["payload_length"] = tupled[5]

        if(parsed["payload_length"] > 0):
            fmt=">" + str(parsed["payload_length"]) + "s"
            payload=struct.unpack(fmt, message[10:10+parsed["payload_length"]])[0]
            parsed["payload"] = payload.decode()

        return parsed

    def lcp_generate_message(self, msg, payload):

        if(payload is not None):
            fmt=">" + str(len(payload)) + "s"
            bin_payload=struct.pack(fmt, payload.encode())
            msg["payload_length"] = len(payload)
        else: 
            msg["payload_length"] = 0

        binmsg = p_sf(
                    (msg["V"] << 6) | (msg["T"] << 4) | (msg["P"] << 2) | (msg["R"]), 
                    (msg["code_high"] << 4) | (msg["code_low"]), 
                    msg["message_id"], 
                    int(msg["source_id"]),
                    int(msg["dest_id"]),
                    msg["payload_length"]
                )

        if(payload is not None):
            binmsg+=bin_payload
  
        return binmsg

    def lcp_make_response(self, src, dst, rspcode, msgid, payload):
        
        # msg = dict()
        msg = deepcopy(lcp_msg_template)
        msg["V"] = 1
        msg["T"] = 2
        if(payload is None):                msg["P"] = 0
        elif(isinstance(payload, str)):     msg["P"] = 3
        else:                               msg["P"] = 2
        msg["R"] = 0
        msg["code_high"] = int(rspcode/100)
        msg["code_low"] = int(rspcode%100)
        msg["message_id"] = msgid
        msg["source_id"] = src
        msg["dest_id"] = dst
        if(payload is not None):
            msg["payload_length"] = len(payload)
            if(isinstance(payload, str)):  msg["P"] = 3
            else: msg["P"] = 2
        msg["payload"] = payload

        self.PrintEventLog(self.EVENT_INFO, "[RSP SENT]")
        self.lcp_print_message(msg)
        return self.lcp_generate_message(msg, payload)

    def lcp_make_request(self, method, src, dst, payload):
        msg = deepcopy(lcp_msg_template)
        
        msg["code_high"] = 0
        msg["code_low"] = method
        msg["message_id"] = self.message_id
        msg["source_id"] = src
        msg["dest_id"] = dst
        if(payload is not None):
            msg["payload_length"] = len(payload)
            if(isinstance(payload, str)):  msg["P"] = 3
            else: msg["P"] = 2
        msg["payload"] = payload
        
        self.message_id+=1

        self.PrintEventLog(self.EVENT_INFO, "[REQ SENT]")
        self.lcp_print_message(msg)
        return self.lcp_generate_message(msg, payload)

    def lcp_respond(self, src, dst, rspcode, msgid, payload):
        
        # print("Send Response : ", rspcode)
        response_msg = self.lcp_make_response(    
                                src=src,
                                dst=dst,
                                rspcode=rspcode,      
                                msgid=msgid,
                                payload=payload
        )

        self.send(response_msg)

    def lcp_register(self, src, dst, payload):
        message = self.lcp_make_request(sfdef.METHOD_REG, src=src, dst=dst, payload=payload)
        self.send(message)
        

    def lcp_put(self, src, dst, payload):
        message = self.lcp_make_request(sfdef.METHOD_PUT, src=src, dst=dst, payload=payload)
        self.send(message)    

    def lcp_get(self, src, dst, payload):
        message = self.lcp_make_request(sfdef.METHOD_GET, src=src, dst=dst, payload=payload)
        self.send(message)    

    def lcp_post(self, src, dst, payload):
        message = self.lcp_make_request(sfdef.METHOD_POST, src=src, dst=dst, payload=payload)
        self.send(message)


        

if __name__ == "__main__":

    ipa=lcp()
    ipa.listen(5000)
    


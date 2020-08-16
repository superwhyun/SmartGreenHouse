from socket import *
import struct
import threading
from eventlogger import EventLogger 


# IP Adaptor Layer의 역할
#  - node id와 IP address가 맵핑 정보를 유지한다
#  - dst id만으로 적절한 IP address로 메시지를 전달한다.

# API
#    - Listen()
#    - Send()
#    - OnRecv()
# 생성자는 OnRecv()에 대한 Callback을 인자로 받아들임.

def u16(x): return struct.unpack('>H', x)[0]

class IpAdaptor(EventLogger):
    # server_socket = socket()
    addressmap = dict()

    
    # API
    ###################################-- <begin> --##################################################
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) 
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
           
        return

    def netif_addressmap_add(self, nodeid, ip, port):
        self.addressmap[nodeid] = (ip, port)

    def send(self, message):
        dest_node_id = u16(message[6:8])
        # print(";", dest_node_id, ";", self.addressmap)
        addr = self.addressmap.get(dest_node_id)
        if(addr is None):
            print("addressmap failure : ", dest_node_id)
            return
        self.socket.sendto(message, addr)
        # print("SEND to ", addr)

    def onrecv(self, message, address):
        pass

    def run(self, port):
        t1 = threading.Thread(target=self.listen, args=(port,))
        t1.daemon=True
        t1.start()
    ###################################-- <end> --##################################################

    def _test_port(self, PORT):
        while True:
            s = socket(AF_INET, SOCK_DGRAM)
            try:
                s.bind(('', PORT)) ## Try to open port
            except OSError as e:
                if e.errno is 48: ## Errorno 98 means address already bound
                    return True
                raise e
            s.close()
            return False



    def listen(self, port, strict=True):
        
        listen_port = 0
        if(strict is False):
            while True:
                if( self._test_port(port) is False):
                    listen_port = port
                    break
                else: port+=1
        else:
            listen_port = port
        
        self.socket.bind(('', listen_port))
        
        # print("LISTENING on ", listen_port)
        while True:
            message, address = self.socket.recvfrom(1024)
            self.addressmap[u16(message[4:6])]=address
            # print(self.addressmap)
            # serverSocket.sendto(message, address)

            self.onrecv(message, address)

            # str=message.decode()
            # msg = json.loads(str)




if __name__ == "__main__":

    ipa=IpAdaptor()
    ipa.listen(5000)
    



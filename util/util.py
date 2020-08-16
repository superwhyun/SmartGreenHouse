import yaml, json
import threading

## TODO: mutex 를 고려해 볼 필요가 초쿰 있다. 일단은 구찮..
class Timer():

    condition=True

    def start(self):
        self.count = 0
        self.timeout_func = None
        self.param = None
        self.period = 0
        self.timer_func()

    def terminate(self):
        self.condition = False
        self.timeout_func = None
        print('terminate timer')

    def set_timer(self, period, func, param):
        
        if(period ==0): 
            self.stop_timer()
            return

        print("set_timer - ", param)
        self.timeout_func = func
        self.param = param
        self.period = period

    def stop_timer(self):
        self.timeout_func = None
        self.param = None
        self.period = 0

    def timer_func(self):
        if(self.condition==True):
            
            # print("count", self.count, " --comp-- ", self.period)
            self.timer=threading.Timer(1.0, self.timer_func)
            self.timer.start()
            self.count += 1.0
            if(self.count >= self.period): 
                if(self.timeout_func is not None):
                    self.timeout_func(self.param)
                    # print('timer fired')
                self.count = 0
        else:
            print('timer terminated')



class DictQuery(dict):
    def get(self, path, default = None):
        keys = path.split("/")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    # val = [ v.get(key, default) if v else None for v in val]
                    for v in val:
                        if( v.get(key, default) ): val=v
                        else: val=None
                else:
                    val = val.get(key, default)
                    # print(val, key)
            else:
                val = dict.get(self, key, default)

            if not val:
                break
        return val
    
    def query(self, query_str):
        query_token = query_str.split("/")
        keyword = query_token[-1].split(":")

        if(len(keyword)==1):
            return DictQuery(self).get(query_str)
    
        query_token.pop()
        path='/'.join(query_token)
        val = DictQuery(self).get(path)
        res=list()
        found = bool()
        if isinstance(val, list):
            for dic in val:
                for k, v in dic.items():
                    if(k == keyword[0] and v == int(keyword[1])): 
                        res.append(dic)
                        found=True
                        break 

        if(found): return res
        else: return None

    def set(self, query_str, replace_value):
        query_token = query_str.split("/")
        keyword = query_token[-1].split(":")

        if(len(keyword)==1):
            return DictQuery(self).get(query_str)
    
        query_token.pop()
        path='/'.join(query_token)
        val = DictQuery(self).get(path)
        
        found = False
        i=0
        if isinstance(val, list):
            for dic in val:
                for k, v in dic.items():
                    if(k == keyword[0] and v == keyword[1]): 
                        val[i] = replace_value
                        found=True
                        break 
                    
                if(found==True): break
                i+=1
            

        return found
        

if __name__ == "__main__":

    fd = open("../sensor_node_cfg.yaml",'r')
    config = yaml.load(fd)

    query="DEVICE/id:2"
    print("RES :", DictQuery(config).query(query))

    query="DEVICE"
    print("RES :", DictQuery(config).query(query))

    query="DEVICE/type:temperature"
    print("RES :", DictQuery(config).query(query))



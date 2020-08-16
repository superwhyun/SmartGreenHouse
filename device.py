import json
import util.util as util





class device:
    def __init__(self):
        self.device_profile = dict()
        pass
        
        
    def device_getstatus(self, query):       
        if(query is not None):
            # print(query)
            val = util.DictQuery(self.device_profile).query(query)
            return val
        else:
            payload = None

        return payload


    def device_setstatus(self, cmd):
        val = util.DictQuery(self.device_profile).query(cmd["TargetID"])  
        if(val is None): return None
        for one in val:    
            for k,v in cmd.items():

                ## TODO: data간의 relationship에 대해서 생각해 봐야 할 듯 하다.

                if  (k == 'TargetID' or k == 'FeedbackRequest'): pass
                elif(k == 'OperationCommand'): one["OperationStatus"] = v
                else: one[k]=v
                
            util.DictQuery(self.device_profile).set(cmd.get('TargetID'), one) 
        return util.DictQuery(self.device_profile).query(cmd["TargetID"])
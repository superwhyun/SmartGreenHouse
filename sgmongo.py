
import pymongo
import sys



class SGmongo:
    def __init__(self):
        pass    


    def _savedata(self, col, data):
        i = 0
        for item in data:
            try:
                col.insert(item)
                i = i+1
            except:
                print("insert failed",sys.exc_info()[0])

        return i
    
    def getControllerNodeInfo(self):
        connection = pymongo.MongoClient("mongodb://localhost")
        db = connection.SmartGreenHouseDB       
        collection = db.ControllerTBL  

        query= {}
        try:
            result = collection.find(query)
        except:
            print("find failed",sys.exc_info()[0])        

        return list(result)

    def saveControllerNodeInfo(self, node_info):
        connection = pymongo.MongoClient("mongodb://localhost")
        db = connection.SmartGreenHouseDB       
        collection = db.ControllerTBL  

        try:
            collection.find_and_modify(query={"NODE.nodeid" : node_info["NODE"]["nodeid"]}, update={"$set" : node_info}, upsert=True, full_response= True)
        except:
            print("find_and_modify failed",sys.exc_info()[0])

        return

    def getDevStatusInfo(self):
        connection = pymongo.MongoClient("mongodb://localhost")
        db = connection.SmartGreenHouseDB       
        collection = db.DevStatusTBL  

        query= {}
        try:
            result = collection.find(query)
        except:
            print("find failed",sys.exc_info()[0])        

        return list(result)

    def saveDevStatusInfo(self, status):
        connection = pymongo.MongoClient("mongodb://localhost")
        db = connection.SmartGreenHouseDB       
        collection = db.DevStatusTBL  
        
        try:
            collection.insert(status)
        except:
            print("collection.insert failed",sys.exc_info()[0])

        return          

    def getDevNodeInfo(self):
        connection = pymongo.MongoClient("mongodb://localhost")
        db = connection.SmartGreenHouseDB       
        collection = db.DevNodeTBL  

        query= {}
        try:
            result = collection.find(query)
        except:
            print("find failed",sys.exc_info()[0])        

        return list(result)

    def saveDevNodeInfo(self, node_info):
        connection = pymongo.MongoClient("mongodb://localhost")
        db = connection.SmartGreenHouseDB       
        collection = db.DevNodeTBL  

        try:
            collection.find_and_modify(query={"NODE.nodeid" : node_info["NODE"]["nodeid"]}, update={"$set" : node_info}, upsert=True, full_response= True)
        except:
            print("find failed",sys.exc_info()[0])

        return
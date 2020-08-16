from flask import Flask, request, render_template
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
import sgmongo
import threading
import sys

class SGC(Resource):
    def get(self):
        dbif = sgmongo.SGmongo()
        controller_list=dbif.getControllerNodeInfo()

        result=list()
        for item in controller_list:
            result.append(item["NODE"])
    
        return jsonify(result)

    def put(self):
        pass

class SGN(Resource):
    def get(self):
        dbif = sgmongo.SGmongo()
        controller_list=dbif.getDevNodeInfo()

        result=list()
        for item in controller_list:
            del item['_id']
            result.append(item)
    
        return jsonify(result)

    def put(self):
        pass

class SGD(Resource):
    def get(self):
        dbif = sgmongo.SGmongo()
        devstat=dbif.getDevStatusInfo()
        
        result=list()
        for item in devstat:
            del item['_id']
            result.append(item)
    
        return jsonify(result)

    def put(self):
        pass

class myFLASK():
    def __init__(self, name):
        self.app = Flask(name)
        self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        self.api = Api(self.app)
        self.api.add_resource(SGC, '/sgc')
        self.api.add_resource(SGN, '/sgn')
        self.api.add_resource(SGD, '/sgd')
    
    def loop(self, flag):
        self.app.run(port='5002')

    def run(self):
        t1 = threading.Thread(target=self.loop, args=(False,))
        t1.daemon=True
        t1.start()

if __name__ == '__main__':

    restful = myFLASK(__name__)
    restful.run()

    # app = Flask(__name__)
    # app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    # api = Api(app)


    def stdin_menu(flag):
        for line in sys.stdin:
            line = line.split()
            if(len(line) >0):
                if(line[0]=='1'): pass
                elif(line[0]=='0'): sys.exit(1)
            else:
                pass

            print("-----")


    stdin_menu(True)

    # t1 = threading.Thread(target=stdin_menu, args=(False,))
    # t1.daemon=True
    # t1.start()





    # @app.route('/')
    # def index():
    #     return render_template('./html/index.html')

    # api.add_resource(SGC, '/sgc')
    # api.add_resource(SGN, '/sgn')

    # app.run(port='5002')




    
    
    # 
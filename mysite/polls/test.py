# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from flask import Flask,request

import flask_restful
from flask_restful import Resource

app = Flask(__name__)
api = flask_restful.Api(app)

todos={}

class HelloWorld(flask_restful.Resource):
    def get(self):
        return {'hello': 'world'}


class TodoSimple(Resource):
        def get(self, todo_id):
            return {todo_id: todos[todo_id]}

        def put(self,todo_id):
	    #todos[hostname] = request.form['hostname']
            todos[todo_id] = request.form['data']
	    #url = "http://192.168.10.61:8088/zbx/api_jsonrpc.php"
       	    #headers = {'content-type': 'application/json'}
       	    #change = json.dumps(
       	    #        {
       	    #    "jsonrpc": "2.0",
       	    #    "method": "trigger.update",
       	    #    "params": {
       	    #        "hostid":'10258',
       	    #        "triggerid": '16318',
       	    #        "status": 1
       	    #    },
       	    #    "auth": "e40f54a7efb0671b54073832e51693de",
       	    #    "id": 1
       	    #    }
       	    #    )

    	    #e = requests.post(url, data=change, headers=headers)
            return {todo_id: todos[todo_id]}



#api.add_resource(HelloWorld, '/')
api.add_resource(TodoSimple, '/<string:todo_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0')

import json,requests
from flask import request, abort,jsonify
import flask_restful as restful
from flask_restful import reqparse
from web_app import app, api, mongo,get_json;
from bson.objectid import ObjectId

url = 'https://mailgnome.herokuapp.com/check_email/';

class EmailList(restful.Resource):
    def __init__(self, *args, **kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('reading',type=str)
        super(EmailList,self).__init__()
        
    def get(self):
        return [x for x in mongo.db.emails.find()]
        
        
    def post(self):
        #get post json data using resquest's get_json method
        data = request.get_json()
        if not data:
            data = {"response": "request cannot be empty!"}
            return jsonify(data)
        if 'email' not in data:
            data = {"response": "No email found!"}
            return jsonify(data)
        
        if "C88B933A691E16C56EBC92BCC9A7E" not in data.values():
            data = {"response": "Unauthorized user"};
            return jsonify(data)
            
        else:
            res =  get_json(url,data)
            print("response:",res);
            print("data:",data)
            data['status'] = res['message'];
            
            print("In resources")
            print(type(data))
            del data['key']
            client_id = mongo.db.emails.insert(data)
            print(client_id);
            return mongo.db.emails.find_one({"_id":client_id})
        pass
        
    def delete(self):
        count = mongo.db.emails.count()
        mongo.db.emails.remove({})
        return jsonify({"response":"delete succesfull","delete_count": count})
         
        
        

class Email(restful.Resource):
    def get(self, client_id):
        return mongo.db.emails.find_one_or_404({"_id":client_id})
    
    def delete(self, client_id):
        mongo.db.emails.find_one_or_404({"_id":client_id})
        mongo.db.emails.remove({"_id":client_id})
        return jsonify({"response":"delete succesfull"})
        
    def put(self,client_id):
        data = mongo.db.emails.find_one_or_404({"_id":client_id})
        data = get_json(url,data);
        #print(data)
        resp =  mongo.db.emails.update({'_id': client_id}, data)
        if resp['ok'] == 1:
            return jsonify({"response":"update succesfull"});
        else:
            return jsonify({"response":"update failed"});
        #return jsonify(data)

class Root(restful.Resource):
    def get(self):
        return {
            'status' : 'OK',
            'mongo': str(mongo.db)
        }
api.add_resource(Root, '/api/')
api.add_resource(EmailList, '/api/email/')
api.add_resource(Email, '/api/email/<ObjectId:client_id>')
import os,requests
from flask import Flask,url_for,render_template,jsonify,request
import flask_restful as restful
from flask_pymongo import PyMongo
from flask import make_response
from bson.json_util import dumps
#Define the Mongo url
MONGO_URI = os.environ.get('MONGODB_URI')
#MONGO_URI = "mongodb://admin:admin123@ds149134.mlab.com:49134/heroku_2g2nnp30"

if not MONGO_URI:
    MONGO_URI = "mongodb://localhost:27017/api";
print("MONGO_URL: "+MONGO_URI)




#M Define the WSGI application object
app = Flask(__name__)

app.config['MONGO_URI'] = MONGO_URI

#Initialize mongoDB connection
mongo = PyMongo(app)


#url 
# os.environ['NO_PROXY'] = '127.0.0.1'


#JSON-response builder function
def output_json(obj, code, headers = None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

#gets the email status
def get_json(url,data):
    #url = 'https://mailgnome.herokuapp.com/check_email/'
    email = data['email']
    r = requests.get(url+email.lower());
    print(r)
    data = r.json();
    return data;        


DEFAULT_REPRESENTATIONS = {'application/json': output_json}

api = restful.Api(app)
api.representations = DEFAULT_REPRESENTATIONS


import web_app.resources


@app.route('/')
def index():
    #get complete email list
    return render_template('index.html');


#  if __name__ == '__main__':
#     app.run(host='0.0.0.0',port=8080,debug=True)


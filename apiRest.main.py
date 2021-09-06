from User import User
from flask import Flask, request
from flask_cors import CORS
import json



app = Flask(__name__);
cors = CORS(app, resources={r"/*": {"origins": "*"}});


@app.route("/Comproba", methods = ['POST'])
def Check():
    return DoIt(lambda user:user.IsOk());

@app.route("/Alta", methods = ['POST'])
def Alta():
    return DoIt(lambda user:user.Alta());

@app.route("/Baixa", methods = ['POST'])
def Baixa():
    return DoIt(lambda user:user.Baja());

@app.route("/Actualitza", methods = ['POST'])
def Actualitza():
    return DoIt(Update);

def Update(user):
    user.Update();
    return {
            'password':user.Password,
            'date':str(user.DataRenovacio).split(" ")[0]
        };

def GetUser():
    if request.is_json:
        user= User(request.json["user"],request.json["password"]);
    else:
        user= None;
    return user;

def DoIt(method):
    user=GetUser();
    if user is None:
        response=json.dumps({'error':True,'result':'only json'});
    else:
        response= json.dumps({'error':False,'result':method(user)});

    return response;

if __name__ == '__main__':
    app.run(port='5002');
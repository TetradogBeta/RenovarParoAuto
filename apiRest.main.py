from User import User
from flask import Flask, request
from flask_cors import CORS

from datetime import datetime
from zoneinfo import ZoneInfo
import json


port=5002;
app = Flask(__name__);
cors = CORS(app, resources={r"/*": {"origins": "https://tetradogbeta.github.io/RenovarParoAuto/*"}});#

@app.route("/Check", methods = ['POST'])
def Check():
    return DoIt(lambda user:user.IsOk());

@app.route("/UpState", methods = ['POST'])
def Alta():
    return DoIt(lambda user:user.UpState());

@app.route("/DownState", methods = ['POST'])
def Baixa():
    return DoIt(lambda user:user.DownState());

@app.route("/UpdateState", methods = ['POST'])
def Actualitza():
    return DoIt(Update);

def Update(user):
    user.UpdateData();
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

def DoIt(getResult):
    #miro el horario
    if IsServerWakeUp():
        user=GetUser();
        if user is None:
            response=json.dumps({'error':True,'result':'només json'});
        else:
            response= json.dumps({'error':False,'result':getResult(user)});
    else:
        response=json.dumps({'error':True,'result':"el servidor de www.oficinadetreball.gencat.cat només treballa de dilluns a dissabte de 8-23"});

    return response;
def IsServerWakeUp():
    date=datetime.now(ZoneInfo("Europe/Madrid"));
    diaDeLaSemana=date.weekday();
    isWakeUp=diaDeLaSemana!=6;#domingo=6
    if isWakeUp:
        isWakeUp=date.hour>=8 and date.hour<23;
    return isWakeUp;


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=str(port),debug=False);

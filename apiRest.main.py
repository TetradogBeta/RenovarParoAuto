from User import User
from flask import Flask

import json



app = Flask(__name__);


@app.route("/Comproba", methods = ['POST'])
def Check():
    return json.dumps({'result':GetUser(request).IsOk()});

@app.route("/Alta", methods = ['POST'])
def Alta():
    return json.dumps(result=GetUser(request).Alta());

@app.route("/Baixa", methods = ['POST'])
def Baixa():
    return json.dumps(result=GetUser(request).Baja());

@app.route("/Actualitza", methods = ['POST'])
def Actualitza():
    return json.dumps(result=GetUser(request).Update());

def GetUser(request):
    return User(request.form.get("user"),request.form.get("password"));

if __name__ == '__main__':
    app.run(port='5002');
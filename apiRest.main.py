from User import User
from flask import Flask, request
from flask_cors import CORS


from datetime import datetime
from zoneinfo import ZoneInfo
import json

from OpenSSL import crypto, SSL

certificate="certificate.pem";
private="private.pem";
port=5002;
app = Flask(__name__);
cors = CORS(app, resources={r"/*": {"origins": "https://tetradogbeta.github.io/RenovarParoAuto/*"}});#
#falta /Dardo
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



def GenSSL(
    emailAddress="gabriel.cat.developer@gmail.com",
    commonName="GabrielCatDeveloper",
    countryName="es",
    localityName="Girona",
    stateOrProvinceName="Girona",
    organizationName="GabrielCatDeveloper",
    organizationUnitName="GabrielCatDeveloper",
    serialNumber=4546485,
    validityStartInSeconds=0,
    validityEndInSeconds=10*365*24*60*60,
    keyFile = "private.key",
    certFile="selfsigned.crt"):
    #can look at generated file using openssl:
    #openssl x509 -inform pem -in selfsigned.crt -noout -text
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = countryName
    cert.get_subject().ST = stateOrProvinceName
    cert.get_subject().L = localityName
    cert.get_subject().O = organizationName
    cert.get_subject().OU = organizationUnitName
    cert.get_subject().CN = commonName
    cert.get_subject().emailAddress = emailAddress
    cert.set_serial_number(serialNumber)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(validityEndInSeconds)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha512')
    with open(certFile, "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    with open(keyFile, "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))

if __name__ == '__main__':
    GenSSL(keyFile=private,certFile=certificate);
    app.run(host="0.0.0.0",port=str(port),debug=False,ssl_context=(certificate, private));

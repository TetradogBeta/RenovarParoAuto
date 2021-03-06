import requests
import datetime

class User:
    UrlFuncions="https://www.oficinadetreball.gencat.cat/socfuncions";
    NIE='E';
    DNI='D';
    CampoDNI='dni';#numero y letra
    CampoNIE='nie';#E/D
    CampoPIN='tarjeta';
    Proxies = {
            	#"http": "",
            	#"http": "",
    };

    def __init__(self,user,password):
        if User.IsNumber(user[0]):
            self.TipoDNI=User.DNI;
        else:
            self.TipoDNI=User.NIE;
        self.User=user.upper();
        self.Password=password.upper();
        self._Session=None;
        self.DataRenovacio=None;
    @property
    def Session(self):
        if self._Session is None:
            relUrl="/LoginNifCodi.do";
            payload={
                User.CampoDNI:self.User,
                User.CampoPIN:self.Password,
                User.CampoNIE:self.TipoDNI,
                "urlDesti":"Renovacio.do",
                "botonInput":"Acceptar",
            };
            try:
                self._Session= requests.Session();
                response = self._Session.post(User.UrlFuncions+relUrl, data=payload, proxies=User.Proxies);
                if response.status_code == 200:
                    try:
                        correcte="RENOVAR LA DEMANDA" in str(response.content);
                        
                    except:
                        raise Exception("Error al parsear la info");    
                else:
                    raise Exception("Usuario y/o contraseña equivocados y quizás el tipo también!");
            except:
                self._Session=None;

        return self._Session;
    
    def IsOk(self):
        return self.Session is not None;
        

    def UpdateState(self):
        self.UpState();
        relUrl="/ResultatRenovacioT.do";
        btn="botonInput";
        value="Renovar la demanda";
        payload={
            btn:value
        };
        
        response = self.Session.post(User.UrlFuncions+relUrl, data=payload, proxies=User.Proxies);
        if response.status_code == 200:
            try:
                content=str(response.content);
                correcte="per la qual cosa no podeu renovar la" not in content;
            except:
                raise Exception("Error al fer login/donar d'alta");
        else:
            correcte=False;
        return correcte;

    def UpState(self):
        self.DownState();
        relUrl="/ControlCanviSituacioAdm.do";
        payload={
            "accio":"altainscripcio",
            "origen":"baixa",
            "botonInput":"Alta per inscripció",
            "submitDummy":""
            
        };
        response = self.Session.post(User.UrlFuncions+relUrl, data=payload, proxies=User.Proxies);
        if response.status_code == 200:
            try:
                content=str(response.content);
                correcte="S'ha detectat un error. En aquest moment el servei no està disponible." not in content;
            except:
                raise Exception("Error donar d'alta");
        elif response.status_code == 404:
            correcte=True;#respuesta cuando ya está dado de alta. o se dió de baja voluntaria...mirar de dar de alta!
        else:
            correcte=False;
        return correcte;

    def DownState(self):
        relUrl="/ControlCanviSituacioAdm.do";
        payload={
            "accio":"baixavoluntaria",
            "origen":"alta",
            "botonInput":"Baixa voluntària",
            "submitDummy":""
            
        };
        response = self.Session.post(User.UrlFuncions+relUrl, data=payload, proxies=User.Proxies);
        if response.status_code == 200:
            try:
                content=str(response.content);
                correcte="Si decidiu tornar a donar-vos" not in content;
            except:
                raise Exception("Error donar d'alta");
        elif response.status_code == 404:
            correcte=True;#respuesta cuando ya está dado de alta. o se dió de baja voluntaria...mirar de dar de alta!
        else:
            correcte=False;
        return correcte;

    def UpdateData(self):
        self.UpdateState();
        relUrl="/PeticioDardo.do";
        response = self.Session.post(User.UrlFuncions+relUrl, data={}, proxies=User.Proxies);
        content= str(response.content);
        self.Password=content.split("Paraula de pas (PIN):&nbsp;\\n\\t\\t\\t\\t\\t\\t\\t&nbsp;")[1].split("</li>")[0];
        self.DataRenovacio=datetime.datetime.strptime(content.split("DATA PROPERA RENOVACI\\xd3</p>\\n<ul id=\"negrita\">")[1].split("</ul>")[0].replace(" ",""),'%d-%m-%Y');

    
    @staticmethod #https://www.geeksforgeeks.org/implement-isnumber-function-in-python/
    # Implementation of isNumber() function
    def IsNumber(s):
        
        # handle for negative values
        isNum=s!=None and s!="";
        if isNum:
            negative = False
            if(s[0] =='-'):
                negative = True;
                
            if negative == True:
                s = s[1:];
            
            # try to convert the string to int
            try:
                dummy = int(s)
                isNum= True;
            # catch exception if cannot be converted
            except ValueError:
                isNum= False;
        return isNum;


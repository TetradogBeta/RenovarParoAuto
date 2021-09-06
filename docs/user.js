


class User{

    constructor(user,password){
        const NIE='E';
        const DNI='D';
        if(isNaN(user[0])){
            this._DNIType=DNI;
        }else{
            this._DNIType=NIE;
        }
        this._Password=password.toUpperCase();
        this._User=user.toUpperCase();
    }
    get User(){
        return this._User;
    }
    get Password(){
        return this._Password;
    }
    get DNIType(){
        return this._DNIType;
    }
    get LoginFormData(){
        var data=new FormData();
        data.append('dni',this.User);
        data.append('tarjeta',this.Password);
        data.append('nie',this.DNIType);
        data.append("urlDesti","Renovacio.do");
        data.append("botonInput","Acceptar");
        return data;
    }
    get UpdateStateFormData(){
        var data=new FormData();
        data.append("botonInput","Renovar la demanda" );
        return data;
    }
    get UpStateFormData(){
        var data=new FormData();
        data.append("accio","altainscripcio");
        data.append("origen","baixa");
        data.append("botonInput","Alta per inscripció");
        data.append("submitDummy","");
            
        return data;
    }
    get DownStateFormData(){
        var data=new FormData();
        data.append( "accio","baixavoluntaria");
        data.append( "origen","alta");
        data.append( "botonInput","Baixa voluntària");
        data.append( "submitDummy","");
        return data;          
        
    }

    Login(){
        return User._DoIt(User.UrlLogin,this.LoginFormData);
    }
    DownState(){
        return User._DoIt(User.UrlDownState,this.DownStateFormData);
    }
    UpState(){
        return User._DoIt(User.UrlUpState,this.UpStateFormData);
    }
    UpdateState(){
        return User._DoIt(User.UrlUpdateState,this.UpdateStateFormData);
    }

    static get UrlUpdateState(){
        return User.UrlFuncions+"/ResultatRenovacioT.do";
    }
    static get UrlUpState(){
        return User.UrlFuncions+"/ControlCanviSituacioAdm.do";
    }
    static get UrlDownState(){
        return User.UrlFuncions+"/ControlCanviSituacioAdm.do";
    }
    static get UrlDardo(){
        return User.UrlFuncions+"/PeticioDardo.do";
    }
    static get UrlLogin(){
        return User.UrlFuncions+"/LoginNifCodi.do";

    }
    static get UrlFuncions(){
        return "https://www.oficinadetreball.gencat.cat/socfuncions";
    }

    static _DoIt(url,formData){
        return new Promise((resolver,rechazar)=>{
            var xhr = new XMLHttpRequest();
            xhr.open("POST", url,true);
            xhr.withCredentials=true;
            xhr.onload=function(){
                if(this.status==200){
                    resolver(this);
                }
                else{
                    rechazar(this);
                }
            };
            xhr.send(formData);
      

        });
    }



}